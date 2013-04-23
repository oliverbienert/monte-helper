<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="2.0" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	
	<xsl:output encoding="UTF-8"/>
	
	<xsl:template match="root">
		<html>
			<head>
				<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
				<title><xsl:value-of select="title"/></title>
				<link rel="stylesheet" type="text/css" href="default.css"/>
			</head>
			<body>
				<h2><xsl:value-of select="title"/></h2>
				<p>
					Freie Montessorischule Barnim e.V. (FMB e.V.)<br/>
					c/o Vorstand, zuständig: Adrian Bleisch/ Ulf Hoffmann/ Stephan Graupner<br/>
					Friedrich-Engels-Str. 6<br/>
					16225 Eberswalde<br/>
					Tel. 03334-288548
				</p>
				<h3>Stichtag: <xsl:value-of select="date"/></h3>
				<xsl:apply-templates select="children"/>	
			</body>
		</html>
	</xsl:template>

	<xsl:template match="children">
		<table style="margin-bottom: 0.2cm; width: 17cm; border: black 1px solid; font-size: 10pt;  table-layout: fixed;">
			<tr>
				<th class="border" style="width:2.5cm;">Name</th>
				<th class="border" style="width:2.5cm;">Vorname</th>
				<th class="border" style="width:1cm;">Klasse</th>
				<th class="border" style="width:2cm;">Geburtstag</th>
				<th class="border" style="width:3cm;">Adresse</th>
				<th class="border" style="width:2cm;">Ort</th>
				<th class="border" style="width:1cm;">PLZ</th>
				<th class="border" style="width:1cm;">Landkr.</th>
				<th class="border" style="width:1cm;">bis 4/6h</th>
				<th class="border" style="width:1cm;">über 4/6h</th>
			</tr>
			<xsl:apply-templates select="child"/>
		</table>
	</xsl:template>

	<xsl:template match="child">
		<tr>
			<td class="border"><xsl:value-of select="name"></xsl:value-of></td>
			<td class="border"><xsl:value-of select="firstname"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="year_id"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="birthdate"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="address"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="city"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="postcode"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="district"></xsl:value-of></td>
			<td class="border" style="text-align:right;">
				<xsl:if test="exdt != '1'">x</xsl:if>
			</td>
			<td class="border" style="text-align:right;">
				<xsl:if test="exdt = '1'">x</xsl:if>
		    </td>
		</tr>
	</xsl:template>
	
</xsl:stylesheet>
