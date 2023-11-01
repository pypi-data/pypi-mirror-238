# -*- coding: utf-8 -*-
from htag import Tag
import htbulma as b
import html,sys

__version__ = "0.1.0" # auto generated

def profile( pyfile:str ) -> list:
    import cProfile
    return cProfile.Profile().run(open(pyfile).read()).getstats()

class ppviz(Tag.body):
    statics="""
    span.code {font-size:0.7em;font-family: monospace;float:right}
    span.local {font-weight:800}
    """
    def init(self):
        self["class"]="content"
        self.pyfile=""
        self.select=None
        self.stats, self.statsroot = [],[]
        self.sortkey=0
        
        self.otitle=Tag.h5()
        self.omain=Tag.div()
        
        self+= self.otitle + self.omain
        
        self.call.analyze()

    def analyze(self):
        try:
            assert len(sys.argv)==2,"You must pass a 'python file' to profile"
            self.pyfile = sys.argv[-1]
            self.stats=profile( self.pyfile )
            self.statsroot = list(self.stats)   # save original
            self.max = max( [i.totaltime for i in self.stats] )
        except Exception as e:
            self.set( html.escape(str(e)) )
        
    def render(self):
        if self.stats:
            def aff(x):
                if hasattr(x,"co_name"):
                    if x.co_filename=="<string>":
                        file,klass = self.pyfile, "local"
                    else:
                        file,klass = x.co_filename, ""
                    try:
                        line = open(file,"r+").read().splitlines()[x.co_firstlineno - 1]
                    except:
                        line= file
                    if x.co_name=="<module>":
                        oinfo = Tag.span(file,_class="code")
                    else:
                        oinfo = Tag.span(line,_title=f"{html.escape(file)}:{x.co_firstlineno - 1}",_class="code")
                    return Tag.span( html.escape(x.co_name),_class=klass) + oinfo
                return html.escape( str(x) )
                
            def event_follow(o):
                self.select=o.select
                self.stats=o.stats
                
            def event_changesort(o): 
                self.sortkey=o.sortkey
                
            table = [ [
                i.callcount,
                int((i.totaltime * 100)/self.max),
                Tag.a(len(i.calls),stats=i.calls,select=i.code,_onclick=event_follow) if hasattr(i,"calls") and i.calls else None ,
                aff(i.code), 
            ] for i in self.stats]
            table.sort( key=lambda row: -row[self.sortkey] )
            
            cols=[Tag.a(title,sortkey=idx,_onclick=event_changesort) for idx,title in enumerate(["call count","%time"])] + ["calls","code"]
            self.omain.set( b.Table( table , cols ) )
        else:
            self.omain.set( b.Progress() )

        if self.select:
            self.otitle.set( Tag.a(self.pyfile,stats = self.statsroot,select=None,_onclick=event_follow) +" : "+ aff(self.select))
        else:
            self.otitle.set( self.pyfile )

def main( ):
    from htag.runners import ChromeApp
    ChromeApp(ppviz).run()

if __name__=="__main__":
    #~ sys.argv=["","t.py"]
    main()    
