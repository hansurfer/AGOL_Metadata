<?xml version="1.0"?>
<!-- Modifed EPA Metadata Editor EMEToolbox EPAUpgradeCleanup.xslt https://github.com/USEPA/EPA-Metadata-Editor-5/blob/master/EMEToolbox/EPAUpgradeCleanup.xslt-->
<!-- Processes ArcGIS metadata to remove Legacy elements. -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:esri="http://www.esri.com/metadata/">
	<xsl:output method="xml" indent="yes" version="1.0" encoding="UTF-8" omit-xml-declaration="no"/>
	
	<!-- start processing all nodes and attributes in the XML document -->
	<!-- any CDATA blocks in the original XML will be lost because they can't be handled by XSLT -->
	<xsl:template match="/">
		<xsl:apply-templates select="node() | @*" />
	</xsl:template>

	<!-- copy all nodes and attributes in the XML document -->
	<xsl:template match="node() | @*" priority="0">    
		<xsl:copy>      
			<xsl:apply-templates select="node() | @*" />
		</xsl:copy>
	</xsl:template>	

    <!-- exclude Legacy elements from the output -->
	<!--<xsl:template match="Esri | Binary | idinfo | dataqual | spdoinfo/indspref | spdoinfo/direct | spdoinfo/ptvctinf/sdtsterm | spdoinfo/ptvctinf/vpfterm | spdoinfo/rastinfo | spref | distinfo | metainfo | Esri/MetaID | Esri/Sync | seqId | MemberName | catFetTyps/*[not(name() = 'genericName')] | scaleDist/uom | dimResol/uom | valUnit/*[not(name() = 'UOM')] | quanValUnit/*[not(name() = 'UOM')] | coordinates | usrDefFreq/*[not(name() = 'duration')] | exTemp/TM_GeometricPrimitive | citId/text() | citIdType | geoBox | geoDesc | MdIdent | RS_Identifier | searchKeys" priority="1" >-->
	<!--</xsl:template>-->
	<xsl:template match="Esri | Binary | idinfo | dataqual | spdoinfo/indspref | spdoinfo/direct | spdoinfo/ptvctinf/sdtsterm | spdoinfo/ptvctinf/vpfterm | spdoinfo/rastinfo | spref | distinfo | metainfo | Esri/MetaID | Esri/Sync | seqId | MemberName | catFetTyps/*[not(name() = 'genericName')] | scaleDist/uom | dimResol/uom | valUnit/*[not(name() = 'UOM')] | quanValUnit/*[not(name() = 'UOM')] | coordinates | usrDefFreq/*[not(name() = 'duration')] | exTemp/TM_GeometricPrimitive | citId/text() | citIdType | geoBox | geoDesc | MdIdent | RS_Identifier" priority="1" >
	</xsl:template>

</xsl:stylesheet>