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
				<p>Beitragsbescheid, gültig ab: <xsl:value-of select="validfromdate"></xsl:value-of></p>
				<h3>Empfänger</h3>
				<xsl:apply-templates select="address"/>
				<h3>Beiträge</h3>
				<p>Gemäß § 17 des Kindertagesstättengesetzes (KitaG Land Brandenburg) vom 27.06.2004  und der von der Mitgliederversammlung zuletzt beschlossenen Beitragsordnung wird Ihr monatlicher Beitrag für die Nutzung der Einrichtungen des Freie Montessorischule Barnim e.V. wie folgt festgesetzt:</p>
				<xsl:apply-templates select="fee" mode="fee"/>
				<h3>Berechnung</h3>
				<xsl:apply-templates select="fee"/>
				<h3>Einkommen</h3>
				<xsl:apply-templates select="income"/>
				<h3>Bemerkungen</h3>
				<xsl:apply-templates select="notes"/>
				<p>Die Elternbeiträge werden zum 15. des Monats eingezogen.</p>
				<p>Für eventuell erforderlich werdende Mahnungen werden jeweils 5,- € Gebühren erhoben.<br/>Veränderungen des Gesamteinkommens von mehr als 5 % müssen dem Vorstand unter Vorlage entsprechender Bescheide zur Kenntnis gegeben werden.</p>
				<p>Dieser Beitragsbescheid ersetzt alle früheren Bescheide.</p>
				<p>Eberswalde, den <xsl:value-of select="today"/></p>
			</body>
		</html>
	</xsl:template>
	
	<xsl:template match="address">
		<p><xsl:apply-templates select="row"/></p>
	</xsl:template>
  
	<xsl:template match="row">
		<xsl:choose>
			<xsl:when test="position()!=last()"><xsl:value-of select="."/><br/></xsl:when>
			<xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="fee" mode="fee">
		<table style="border-width:0;">
			<xsl:apply-templates select="child" mode="fee"/>
		</table>
	</xsl:template>

	<xsl:template match="child" mode="fee">
		<tr>
			<td style="font-weight: bold;"><xsl:value-of select="name"/>, <xsl:value-of select="firstname"></xsl:value-of></td>
			<td style="font-weight: bold;"><xsl:value-of select="fee"/></td>
		</tr>
	</xsl:template>
	
	<xsl:template match="fee">
		<table style="margin-bottom: 0.2cm; width: 17cm; border: black 1px solid; font-size: 10pt;  table-layout: fixed;">
			<tr>
				<th class="border" style="width:3cm;">Name</th>
				<th class="border" style="width:3cm;">Vorname</th>
				<th class="border" style="width:1.5cm;">Eink.</th>
				<th class="border" style="width:1.5cm;">Kinder- geld</th>
				<th class="border" style="width:1.5cm;">Mind. 1</th>
				<th class="border" style="width:1.5cm;">Mind 2</th>
				<th class="border" style="width:1.5cm;">Erw. Betr.</th>
				<th class="border" style="width:1.5cm;">Berücks. Eink.</th>
				<th class="border" style="width:2cm;">Betrag</th>
			</tr>
			<xsl:apply-templates select="child"/>
		</table>
	</xsl:template>
	
	<xsl:template match="child">
		<tr>
			<td class="border"><xsl:value-of select="name"></xsl:value-of></td>
			<td class="border"><xsl:value-of select="firstname"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="income"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="benefit"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="reduction1"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="reduction2"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="extendeddaytime"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="incomeapplied"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="fee"></xsl:value-of></td>
		</tr>
	</xsl:template>
	
	<xsl:template match="income">
		<table style="margin-bottom: 0.2cm; width: 17cm; border: black 1px solid; font-size: 10pt;  table-layout: fixed;">
			<tr>
				<th class="border" style="width:3cm;">Name</th>
				<th class="border" style="width:3cm;">Vorname</th>
				<th class="border" style="width:1.5cm;">Nicht selbst.</th>
				<th class="border" style="width:1.5cm;">Selbst.</th>
				<th class="border" style="width:1.5cm;">Arbeits- amt</th>
				<th class="border" style="width:1.5cm;">Unterhalt</th>
				<th class="border" style="width:1.5cm;">Sonst.</th>
				<th class="border" style="width:1.5cm;">Abzügl.</th>
				<th class="border" style="width:2cm;">Gesamt</th>
			</tr>
			<xsl:apply-templates select="adult"/>
		</table>
	</xsl:template>
	
	<xsl:template match="adult">
		<tr>
			<td class="border"><xsl:value-of select="name"></xsl:value-of></td>
			<td class="border"><xsl:value-of select="firstname"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="salary"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="income"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="unemployment"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="childsupport"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="misc"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="less"></xsl:value-of></td>
			<td class="border" style="text-align:right;"><xsl:value-of select="totalincome"></xsl:value-of></td>
		</tr>
	</xsl:template>
	
	<xsl:template match="notes">
		<p><xsl:call-template name="repNL">
		    <xsl:with-param name="pText" select="."/></xsl:call-template></p>
	</xsl:template>
	
	<xsl:template name="repNL">
		  <xsl:param name="pText" select="."/>
		
		  <xsl:copy-of select=
		  "substring-before(concat($pText,'&#xA;'),'&#xA;')"/>
		
		  <xsl:if test="contains($pText, '&#xA;')">
		   <br />
		   <xsl:call-template name="repNL">
		    <xsl:with-param name="pText" select=
		    "substring-after($pText, '&#xA;')"/>
		   </xsl:call-template>
		  </xsl:if>
	</xsl:template>
	
	
</xsl:stylesheet>
