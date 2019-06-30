<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:output method="text" indent="yes"/>
    
    <xsl:template match="/">
        <xsl:apply-templates select="root/*"/>
        <xsl:apply-templates select="//laureates"/>
    </xsl:template>
    
    <xsl:template match="root/*">
###  http://prc.di.uminho.pt/2019/prizes#<xsl:value-of select="category"/><xsl:value-of select="year"/>
:<xsl:value-of select="category"/><xsl:value-of select="year"/> rdf:type owl:NamedIndividual ,
                            :Prize;
<xsl:for-each select="laureates">
                   :laureates :laureate<xsl:value-of select="id"/> ;
</xsl:for-each>
<xsl:if test="overallMotivation">
                   :overallMotivation "" ;
</xsl:if>
                   :year "<xsl:value-of select="year"/>" ;
                   :category "<xsl:value-of select="category"/>" .
    </xsl:template>
    
    <xsl:template match="laureates">
###  http://prc.di.uminho.pt/2019/prizes#laureate<xsl:value-of select="id"/>
:laureate<xsl:value-of select="id"/> rdf:type owl:NamedIndividual ,
                            :Laureate ;
                   :id "<xsl:value-of select="id"/>" ;
                   :firstname "<xsl:value-of select="firstname"/>" ;
                   :surname "<xsl:value-of select="surname"/>" ;
                   :motivation "" ;
                   :share "<xsl:value-of select="share"/>" .
    </xsl:template>
</xsl:stylesheet>