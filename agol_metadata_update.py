#-------------------------------------------------------------------------------
# Purpose: script to prepare xml metadata and upload to AGOL
#   - remove legacy fgdc elements, geoprocessing history, local storage info, and Metadata copy History
#   - upload metadata to agol
#
# Pre-process:
#   - metadata style must be ArcGIS style. Upgrade metadata if it is FGDC style
#     (gp tool - Upgrade Metadata with "FGDC_TO_ARCGIS" as Upgrade Type
#   - export metadata to c:/temp
#     (gp tool - XSLT Transformation with "exact copy of.xslt" as Input XSLT
#
# Requirements:
#   - AGOL item IDs
#   - xml file(s)
#   - AGOL account with admin privilege
#
# Author:   Sanghong Yoo
# Created:  2018/06/04
# Revised:  2018/12/19
#-------------------------------------------------------------------------------

# Import modules
import time
from os import path
import xml.etree.ElementTree as ET
import lxml.etree as lxmlET
from arcgis import gis
from dateutil.parser import parse

# arcgis metadata xml tags
metaTag = {
"revisedate":   "dataIdInfo/idCitation/date/reviseDate",
"createdate":   "dataIdInfo/idCitation/date/createDate",
"pubDate":      "dataIdInfo/idCitation/date/pubDate",
"procEnviron":  "dataIdInfo/envirDesc",
}

# update ArcGIS Installation Location
remove_local_storage_info_strict = "<ArcGIS Installation Location>/Metadata/Stylesheets/gpTools/remove local storage info strict.xslt"
remove_entries_from_FGDC = "FGDCTagCleanup.xslt"


def parentTagFuc(childTag):
    """
    Return parent tag

    Parameters
    ----------
    childTag: str
        child tag string
    Returns
    -------
    str
        return parent tag
    """
    """Get parent tag"""
    templist = childTag.split("/")
    del templist[-1:]
    return "/".join(templist)


def parentTag(Tag):
    """
    Return parent and child tag

    Parameters
    ----------
    tag: str
        tag string
    Returns
    -------
    tuple
        return parent and child tag
    """
    """Get parent tag"""
    templist = Tag.split("/")
    ctag = templist[-1]
    del templist[-1:]
    ptag = "/".join(templist)
    return ptag, ctag


def findaddmissingxmltagNoPrint(input_element):
    """
    Check input element (xml tag) exist in xml file.
    If not, add missing element (xml tag)
    NO Print statement
    """
    # check if input xml element/tag exist
    if tree.find(input_element) is not None:
        return

    # xml elements list
    xml_element_list = input_element.split("/")
    # xml root
    xmlRoot = tree.getroot()

    for j in range(len(xml_element_list), 0, -1):
        # recreate xml tag from xml elements list
        xmltag = "/".join(xml_element_list[0:j])

        # find and add missing child element/tag
        if tree.find(xmltag) is not None:
            temp_xml_tag = xmltag
            for k in range(j, len(xml_element_list)):
                childxml = xml_element_list[k]
                addxmlTag(temp_xml_tag, childxml)
                temp_xml_tag = "/".join(xml_element_list[0:k+1])
            break
        # add if input element/tag doesn't exist
        if j-1 == 0:
            child_element = ET.Element(xmltag)
            xmlRoot.append(child_element)
            temp_xml_tag = xmltag
            for l in range (1, len(xml_element_list)):
                childxml = xml_element_list[l]
                addxmlTag(temp_xml_tag, childxml)
                temp_xml_tag = "/".join(xml_element_list[0:l+1])


def addxmlTag(parentxmltag, chilxmlele):
    """Append child xml element

    Parameters
    ----------
    parentxmltag: str
        parent xml tag
    chilxmlele: str
        chil xml tag
    Returns
    -------
    None
    """
    child_element = ET.Element(chilxmlele)
    parent_element = tree.find(parentxmltag)
    parent_element.append(child_element)


def addxmlText(xmltag, text=""):
    """Add xml text"""
    element = tree.find(xmltag)
    element.text = text


def deleteAllChildXmlTagNoPrint(parentTag):
    """
    Delete all child xml tag(s).
    NO print statement
    """
    #find parent tag - Element object
    elem = tree.find(parentTag)
    #if parent tag element exists
    if elem is not None:
        #loop Element and remove child elements
        for childElem in elem:
            elem.remove(childElem)


def deletexmlTag2NoPrint(childTag):
    """
    Delete xml tag without parent tag
    No print statement
    """
    #get parent tag
    parentTag = parentTagFuc(childTag)
    #find parent tag - Element object
    elem = tree.find(parentTag)
    #if parent tag element exists
    if elem is not None:
        #find child tags - a list with child Elements
        ##            childElem = self.findxmltagAll(childTag)
        childElem = tree.findall(childTag)
        #loop Element and remove child elements
        for child in childElem:
            elem.remove(child)


def deleteElem(tag):
    """
    Delete tag
    """
    #get parent tag
    pTag, cTag = parentTag(tag)
    #find parent tag - Element object
    pElem = tree.find(pTag)
    #if parent tag element exists
    if pElem is not None:
        cElem = pElem.find(cTag)
        if cElem is not None:
            pElem.remove(cElem)


def inputChoice(qprompt):
    try:
        value = int(input(qprompt) or thelatestdate(revDate, pubDate, creDate))
    except ValueError:
        print("Please select from 1, 2, 3, 4, 5")
        return inputChoice(qprompt)

    if value not in [1, 2, 3, 4, 5]:
        print("Please select from 1, 2, 3, 4, 5")
        return inputChoice(qprompt)
    else:
        return value


def is_date(dateText):
    """
    https://stackoverflow.com/questions/25341945/check-if-string-has-date-any-format
    Parameters
    ----------
    dateText

    Returns
    -------

    """

    try:
        return parse(dateText)
    except ValueError:
        return ""


def thelatestdate(revD, pubD, creD):
    """
    compare create, publish, revise and return the latest date as the assigned integer

    Parameters
    ----------
    revD: date
        revised date
    pubD: date
        publication date
    creD: date
        creation date

    Returns
    -------
    lastnum: integer
        latest date for the assigned integer

    """
    # lastnum = 1
    # lastdate = 1
    if is_date(revD):
        if is_date(pubD):
            lastnum = 1 if is_date(revD) >= is_date(pubD) else 2
            lastdate = is_date(revD) if is_date(revD) > is_date(pubD) else is_date(pubD)
        else:
            lastnum = 1
            lastdate = is_date(revD)
        if is_date(creD):
            lastnum = lastnum if lastdate >= is_date(creD) else 3
    elif is_date(pubD):
        lastnum = 2
        if is_date(creD):
            lastnum = lastnum if is_date(pubD) >= is_date(creD) else 3
    elif is_date(creD):
        lastnum = 3
    else:
        lastnum = 4

    return lastnum


# AGOL item ids and metadata xml files. The order must be same.
itemlist = ["<AGOL Item ID", "<AGOL Item ID>"] # AGOL item IDs
xmlpathlist = ["c:/temp/temp1.xml", "c:/temp/temp2.xml"] # exported metadata xml file path.

for counter, xmlfile in enumerate(xmlpathlist):
    print("\n## {} of {}: {}".format(counter + 1, len(xmlpathlist), xmlfile))

    if path.isfile(xmlfile):

        # remove local storage info strict
        print("# Removing geoprocessing history and local storage info")
        dom = lxmlET.parse(xmlfile)
        newdom = lxmlET.XSLT(lxmlET.parse(remove_local_storage_info_strict))(dom)

        # remove entries from FGDC
        print("# Removing FGDC legacy elements")
        newdom = lxmlET.XSLT(lxmlET.parse(remove_entries_from_FGDC))(newdom)

        newdom.write(xmlfile)

        # set xml tree element
        print("# Resetting ArcGIS Style/Format")
        tree = ET.parse(xmlfile)

        deleteAllChildXmlTagNoPrint('Esri') # remove ESRI legacy elements
        findaddmissingxmltagNoPrint('Esri/ArcGISFormat')
        findaddmissingxmltagNoPrint('Esri/ArcGISProfile')
        addxmlText('Esri/ArcGISFormat', '1.0')
        addxmlText('Esri/ArcGISProfile', 'ISO19139')

        print("# Deleting Process Environment Info")
        deletexmlTag2NoPrint(metaTag['procEnviron'])

        ## if you don't need to worry about updating publication date, ##
        ## remove or comment out from line 264 to 326                  ##

        ##                  update publication date               ##
        # Open Data Portal (ArcGIS Hub) only utilize "publication date" in metadata
        # Provide an option to change the publication date from
        # create, publish, revise, or today's date before upload to AGOL.

        revDateElement = tree.find(metaTag["revisedate"])
        pubDateElement = tree.find(metaTag["pubDate"])
        creDateElement = tree.find(metaTag["createdate"])

        if revDateElement is not None:
            revDate = revDateElement.text
        else:
            revDate = ""

        if pubDateElement is not None:
            pubDate = pubDateElement.text
        else:
            pubDate = ""

        if creDateElement is not None:
            creDate = creDateElement.text
        else:
            creDate = ""

        print("\n****************************************")
        print("Revision Date in Metadata   : {}".format(revDate.split("T")[0]))
        print("Publication Date in Metadata: {}".format(pubDate.split("T")[0]))
        print("Creation Date in Metadata   : {}".format(creDate.split("T")[0]))
        print("****************************************")

        qprompt4 = ("\nSelect Date to use?\n"
                   "1: Revision Date\n"
                   "2: Publication Date\n"
                   "3: Creation Date\n"
                   "4: Today\n"
                   "5: Quit\n"
                   "\n"
                   "Enter the choice, the Default date is {}:".format(thelatestdate(revDate, pubDate, creDate)))

        # user input for publication date
        daterowInput = inputChoice(qprompt4)

        if daterowInput == 1:
            pubDate = revDate
        elif daterowInput == 2:
            pubDate = pubDate
        elif daterowInput == 3:
            pubDate = creDate
        elif daterowInput == 4:
            pubDate = time.strftime("%Y-%m-%d") + "T00:00:00"
        else:
            print("\nTerminating the script by user")
            exit()

        # set publication date
        if pubDateElement is None:
            findaddmissingxmltagNoPrint(metaTag["pubDate"])
            pubDateElement = tree.find(metaTag["pubDate"])

        pubDateElement.text = pubDate

        # delete revised and created date
        if revDateElement is not None:
            deleteElem(metaTag["revisedate"])
        if creDateElement is not None:
            deleteElem(metaTag["createdate"])

        tree.write(xmlfile)

    else:
        print("# XML file not found, remove item from the list")
        itemlist.pop(counter)
        xmlpathlist.pop(counter)


print("\n\n****************************************")
print("Enter AGOL Username and Password")

# agol gis container
agousername = input("Username: ")
agopassword = input("Password: ")
gisContainer = gis.GIS(username = agousername, password = agopassword) # agol admin account
print(" ")

for counter2, item in enumerate(itemlist):
    # print(item, xmlpathlist[counter2])
    itemIDtemp = item
    agolitem = gis.Item(gisContainer, itemid = itemIDtemp)

    print("\n## {} of {}: uploading metadata of {}".format(counter2 + 1, len(itemlist), agolitem.title))
    itemProperties = {'typeKeywords': 'Metadata'}
    # xml file upload
    agolitem.update(item_properties=itemProperties, metadata=xmlpathlist[counter2])