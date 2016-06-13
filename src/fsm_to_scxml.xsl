<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://www.w3.org/2005/07/scxml">

<xsl:output method="xml"
                doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
                doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
                encoding="UTF-8"
                indent="yes"
            />


    <xsl:template match="/fsm">
        <scxml version="1.0">
            <xsl:call-template name="states"/>
        </scxml>
    </xsl:template>



<xsl:template name="states">
            <xsl:for-each select="state">
                <xsl:choose>
                    <xsl:when test="@type = 'f'">
                        <xsl:call-template name="finalTranform"/>
                    </xsl:when>
                    <xsl:when test="@type = 'r'">
                        <xsl:call-template name="statesTranform"/>
                    </xsl:when>
                </xsl:choose>
            </xsl:for-each>
</xsl:template>

<xsl:template name="finalTranform">
    <xsl:variable name="stateId" select="@id"/>
    <final id="{$stateId}">
        <xsl:for-each select="transition">
            <xsl:call-template name="transitionTranform"/>
        </xsl:for-each>
    </final>
</xsl:template>

<xsl:template name="statesTranform">
        <xsl:variable name="stateId" select="@id"/>
        <state id="{$stateId}">
            <xsl:for-each select="transition">
                <xsl:call-template name="transitionTranform"/>
            </xsl:for-each>
        </state>
</xsl:template>

<xsl:template name="transitionTranform">
        <xsl:variable name="event" select="@under"/>
        <xsl:variable name="target" select="."/>
        <transition event="{$event}" target="{$target}"/>
</xsl:template>



</xsl:stylesheet>