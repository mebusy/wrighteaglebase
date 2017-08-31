import scrapy
import os
import json
import codecs
import pprint 
pp = pprint.PrettyPrinter(indent=4)


class PlayerSpider( scrapy.Spider ):
    name = "players"
    
    def __init__(self):
        super( PlayerSpider , self ).__init__()

        self.MAX_PLAYER_REQUEST = 4
        self.url_offset_prefix = "https://sofifa.com/players?offset=" 
        self.url_player_prefix = "https://sofifa.com" 
        self.player_offset = 0 

        self.record_file = "./nplayer.txt"
        if os.path.exists( self.record_file ) :
            with open( self.record_file  ) as fp :
                self.player_offset = int( fp.read().strip()  )

    def start_requests(self):
        yield scrapy.Request(url= "{0}{1}".format( self.url_offset_prefix, self.player_offset ) , callback=self.parse)
        
    
    def parse(self, response):
        player_links = response.xpath('//div[normalize-space(@class)="col-name text-clip rtl"]/a[@href and @title][starts-with(@href,"/player/")]/@href')

        if len( player_links ) == 0:
            return 

        self.nplayer2parse = min( self.MAX_PLAYER_REQUEST , len( player_links ) )
        follow_links = player_links[ : self.nplayer2parse ]
        for link in follow_links :
            # url = "{0}{1}".format( self.url_player_prefix , link.extract()  ) 
            yield response.follow( link.extract() , callback=self.parsePlayer ) 

    def parsePlayer( self, response ) :
        print '~~~ parse player:',  response.url 

        p = {}

        nations = response.xpath( '//div[@class="meta"]/span/a[@title]/@title' ).extract() 
        assert( len(nations) == 1 ) 

        p["na"] = nations[0]

        info = response.xpath( '//div[@class="info"]' )
        p["name"],p["id"] = info.xpath( "//h1/text()" ).re(r"(.*?)\s*\(\s*ID:\s*(\d+)\s*\)") 
        
        pts = response.xpath( '//script[contains(text(),"pointPAC")]' ).re( r'var\s+point(\w+)\s*=\s*(\d+)\s*;' ) 
        i = iter(pts)
        dict_pts = dict( zip( i,i ) )
        p.update( dict_pts ) 

        clubs = response.xpath( '//ul/li/a[starts-with( @href , "/team/" )]/text()' ).extract()
        if isinstance( clubs, list ) :
            p["clubs"] = clubs 
        else:
            p["clubs"] = [clubs]


        p["attr"] = {}
        
        v = response.xpath( '//ul[@class="pl"]/li[count(*)=1]/span[starts-with(@class, "label")]/text()'  ).extract() 
        k = response.xpath( '//ul[@class="pl"]/li[count(*)=1]/span[starts-with(@class, "label")]/parent::*/text()'  ).re( r"(\w+(?:\s+\w+)*)" )
        assert( len(k) == len(v) ) 

        p["attr"].update( dict( zip( k, v))  )
    
        # pp.pprint( p ) 
        
        # make dir
        path_player_data = "player_data"
        if not os.path.exists(  path_player_data ) :
            os.makedirs( path_player_data )

        # write data 
        path = os.path.join( path_player_data , "{0}.txt".format( p["id"] )  )
        with codecs.open( path  , "w", "utf-8") as fp :
            fp.write( json.dumps( p  , ensure_ascii=False , sort_keys= True) )


        # parse end

        self.nplayer2parse -= 1

        if self.nplayer2parse == 0:
            self.player_offset += self.MAX_PLAYER_REQUEST 

            with open( self.record_file , "w" ) as fp :
                fp.write( str( self.player_offset  ) )
            
            if self.MAX_PLAYER_REQUEST  > 1: # == 1 just for debug
                yield scrapy.Request(url= "{0}{1}".format( self.url_offset_prefix, self.player_offset ) , callback=self.parse) 
            print "~~~ group parser done "
