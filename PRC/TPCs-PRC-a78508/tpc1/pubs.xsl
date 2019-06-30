<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:functx="http://www.functx.com"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:function name="functx:capitalize-first" as="xs:string?">
        <xsl:param name="arg" as="xs:string?"/>
        
        <xsl:sequence select="
            concat(upper-case(substring($arg,1,1)),
            substring($arg,2))
            "/>
        
    </xsl:function>
    
    <xsl:output method="text" indent="yes"/>
    
    <xsl:template match="/">
        <xsl:apply-templates select="bibliography/*"/>
        <xsl:apply-templates select="//author|//editor"/>
    </xsl:template>
    
    <xsl:template match="bibliography/*">
        <xsl:variable name="idpub" select="@id"/>
### http://prc.di.uminho.pt/2019/pubs#<xsl:value-of select="@id"/>
:<xsl:value-of select="@id"/> rdf:type owl:NamedIndividual ,
                       :<xsl:value-of select="functx:capitalize-first(name(.))"/> ;
            <xsl:for-each select="author">
              :hasAuthor :<xsl:value-of select="@id"/> ;
            </xsl:for-each>
            <xsl:for-each select="editor">
              :hasEditor :<xsl:value-of select="@id"/> ;
            </xsl:for-each>
            <xsl:for-each select="author-ref">
              :hasAuthor :<xsl:value-of select="@authorid"/> ;
            </xsl:for-each>
            <xsl:for-each select="editor-ref">
              :hasEditor :<xsl:value-of select="@authorid"/> ;
            </xsl:for-each>
            <xsl:if test="address">
              :address "<xsl:value-of select="address"/>" ;    
            </xsl:if>
            <xsl:if test="booktitle">
              :booktitle "<xsl:value-of select="booktitle"/>" ;    
            </xsl:if>
            <xsl:if test="chapter">
              :chapter "<xsl:value-of select="chapter"/>" ;    
            </xsl:if>
            <xsl:if test="doi">
              :doi "<xsl:value-of select="doi"/>" ;    
            </xsl:if>
            <xsl:if test="howpublished">
              :howpublished "<xsl:value-of select="howpublished"/>" ;    
            </xsl:if>
            <xsl:if test="isbn">
              :isbn "<xsl:value-of select="isbn"/>" ;    
            </xsl:if>
            <xsl:if test="issn">
              :issn "<xsl:value-of select="issn"/>" ;    
            </xsl:if>
            <xsl:if test="journal">
              :journal "<xsl:value-of select="journal"/>" ;    
            </xsl:if>
            <xsl:if test="month">
              :month "<xsl:value-of select="month"/>" ;    
            </xsl:if>
            <xsl:if test="number">
              :number "<xsl:value-of select="number"/>" ;    
            </xsl:if>
            <xsl:if test="pages">
              :pages "<xsl:value-of select="pages"/>" ;    
            </xsl:if>
            <xsl:if test="publisher">
              :publisher "<xsl:value-of select="publisher"/>" ;    
            </xsl:if>
            <xsl:if test="school">
              :school "<xsl:value-of select="school"/>" ;    
            </xsl:if>
            <xsl:if test="title">
              :title "<xsl:value-of select="title"/>" ;    
            </xsl:if>
            <xsl:if test="uri">
              :uri "<xsl:value-of select="uri"/>" ;    
            </xsl:if>
            <xsl:if test="volume">
              :volume "<xsl:value-of select="volume"/>" ;    
            </xsl:if>
            <xsl:if test="year">
              :year "<xsl:value-of select="year"/>" .    
            </xsl:if>
    </xsl:template>
    
    <xsl:template match="author">
### http://prc.di.uminho.pt/2019/pubs#<xsl:value-of select="@id"/>
:<xsl:value-of select="@id"/> rdf:type owl:NamedIndividual ,
                    :Author ;
        :name "<xsl:value-of select="."/>" .
    </xsl:template>
    
    <xsl:template match="editor">
### http://prc.di.uminho.pt/2019/pubs#<xsl:value-of select="@id"/>
:<xsl:value-of select="@id"/> rdf:type owl:NamedIndividual ,
                    :Editor ;
        :name "<xsl:value-of select="."/>" .
    </xsl:template>
</xsl:stylesheet>