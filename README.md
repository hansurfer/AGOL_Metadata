# ArcGIS Online Metadata Update/Upload
Python3 scripts to clean ArcGIS Metadata Style xml file(s) and upload to ArcGIS Online.
* remove legacy fgdc and ESRI elements, geoprocessing history, local storage info, and Metadata copy History
* upload metadata to agol
* pre-process:
	* metadata style must be ArcGIS style. Upgrade metadata if it is FGDC style 
		* gp tool - [Upgrade Metadata](http://desktop.arcgis.com/en/arcmap/latest/tools/conversion-toolbox/upgrade-metadata.htm) with "FGDC_TO_ARCGIS" as Upgrade Type
	* export metadata 
		* gp tool - [XSLT Transformation](http://desktop.arcgis.com/en/arcmap/latest/tools/conversion-toolbox/xslt-transformation.htm) with "exact copy of.xslt" as Input XSLT
* requirements:
	* AGOL Item IDs
	* xml file(s)
	* ArcGIS Online account with admin privilege
	* [remove local storage info strict.xslt](remove%20local%20storage%20info%20strict.xslt): ESRI ArcGIS Desktop [remove local storage info strict stylesheet](http://desktop.arcgis.com/en/arcmap/latest/manage-data/metadata/process-metadata-using-xslt-transformations.htm).

<br />

### Contains:
* [agol_metadata_update.py](agol_metadata_update.py) - prepare xml metadata file and upload to AGOL. 
	- things to change/replace
		- ArcGIS Desktop Installation Location
		- ArcGIS Online Item IDs
		- xml file paths
	- *if you don't have to update the publication date with other dates such as revised or creation date, you can remove or comment out from line 264 to 326. The default AGOL html rendering engine doesn't show other dates except the publication date and Open Data Portal (ArcGIS Hub) also uses the publication date to update the updated date.*
* [FGDCTagCleanup.xslt](FGDCTagCleanup.xslt): xslt that removes FGDC element. Modifed EPA Metadata Editor EMEToolbox [EPAUpgradeCleanup.xslt](https://github.com/USEPA/EPA-Metadata-Editor-5/blob/master/EMEToolbox/EPAUpgradeCleanup.xslt).
