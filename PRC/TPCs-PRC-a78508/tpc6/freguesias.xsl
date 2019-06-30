<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:functx="http://www.functx.com"
    xmlns:xp="http://www.w3.org/2001/XMLSchema"
    xmlns:xs="http://www.w3.org/2005/Atom"
    xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" 
    xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"
    xmlns:owl="http://www.w3.org/2002/07/owl#"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:xml="http://www.w3.org/XML/1998/namespace"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:function name="functx:capitalize-first" as="xp:string?">
        <xsl:param name="arg" as="xp:string?"/>
        
        <xsl:sequence select="
            concat(lower-case(substring($arg,1,1)),
            substring($arg,2))
            "/>
        
    </xsl:function>
    
    <xsl:param name="dec-file" select="'mapa-grande.xml'"/>
    <xsl:variable name="dec-doc" select="document($dec-file)"/>
    
    <xsl:output method="text" indent="yes"/>
    
    <xsl:template match="/">
        <xsl:apply-templates select="xs:feed/*"/>
       
        <xsl:for-each select="distinct-values(//d:distrito)">
### http://prc.di.uminho.pt/2019/mapa#<xsl:value-of select="functx:capitalize-first(.)"/>
:<xsl:value-of select="functx:capitalize-first(.)"/> rdf:type owl:NamedIndividual,
                    :Distrito;
        :name :<xsl:text>"</xsl:text><xsl:value-of select="."/><xsl:text>"</xsl:text>;
        </xsl:for-each>
        
        <xsl:for-each select="distinct-values(//d:concelho)">
### http://prc.di.uminho.pt/2019/mapa#<xsl:value-of select="functx:capitalize-first(.)"/>
:<xsl:value-of select="functx:capitalize-first(.)"/> rdf:type owl:NamedIndividual,
                    :Concelho;
        :name :<xsl:text>"</xsl:text><xsl:value-of select="."/><xsl:text>"</xsl:text>;
        </xsl:for-each> 
    </xsl:template>
    
    <xsl:template match="xs:feed/*">
### http://prc.di.uminho.pt/2019/mapa#fre<xsl:value-of select="./xs:content/m:properties/d:dicofre"/>
:fre<xsl:value-of select="./xs:content/m:properties/d:dicofre"/> rdf:type owl:NamedIndividual,
                    :Freguesia;
                    :name :<xsl:text>"</xsl:text><xsl:value-of select="./xs:content/m:properties/d:freguesia"/><xsl:text>"</xsl:text>;
                    :dicofre :<xsl:text>"</xsl:text><xsl:value-of select="./xs:content/m:properties/d:dicofre"/><xsl:text>"</xsl:text>;
                <xsl:if test="./xs:content/m:properties/d:brasao">
                    :brasao :<xsl:text>"</xsl:text><xsl:value-of select="./xs:content/m:properties/d:brasao"/><xsl:text>"</xsl:text> .           
                </xsl:if>
        
        
        
                
    </xsl:template>
    
    
</xsl:stylesheet>