import random
import socket
import ssl
import time
from TheSilent.clear import clear

CYAN = "\033[1;36m"

def kiwi(host,delay=0):
    clear()
    hits = []
    init_hosts = []
    hosts = []

    subdomains = ["","aams","accent","accounts","acs-xs","acsamid01","acsids","acsnas","activeapplicant","activeresources","adams","adfs","adm","admin","aes","aesdvr1","aggies","ahs","airwatch","akpk","alt","alumni","ams","angel","aovpn","apache","api","aplus","apple","appleid","apps","apps2","apps3","aps","arabamid","arboretum","archiver","asas","asburyhigh","asg","assessment","atrium","atriuum","attalla","auth","auth2","autodiscover","av","aw","backup","barracuda","barracuda1","bbb","bbcesmoodle","bbchsmoodle","bcbeiboss2","bcboefilewave","bcrobotics","bcsipmonitor","bes","bess-proxy","beverlye","bibbcompass","bibbdestiny","bibbdocumentserver","bigbluebutton","bigboy","blackboard","block","blocker","blogs","bm","bms-audioe","boe-emailsrv","books","bridgit","brindleemiddle","brindleemountainhigh","bsl","buckhornhigh","busshop","butlerco","calendar","carver","casarry","cassidy","causeyband","ccctc","cchs","ccs","certifiedportal","cesmoodle","choice","chsmoodle","ciscoasa","citrix","cl","classlink","classweb","claysville","claysvillejuniorhigh","clearpass1","cloverdale","cms","cmsmoodle","cnp","cobalt","collab-edge","communityeducation","compass","compasslearning","conecuh","cov","cpanel","cpcalendars","cpcontacts","cpi","cppm1","cs-voip","csg","ctcsec","d2l","daleville","dare","darelementary","darhigh","darmiddle","dataservice","datavault","datsrv055","dcsamid01","dcsfws","dcsnamidcl","dcsxserve","ddi","decisioned","dell-learn","des","designthefuture","destination","destiny","dialin","discovervideo","dmm","dmsftp","dn","dns","dns1","docefill","docs","documentservices","domain","donehoo","dothan","dothanhigh","dothantech","douglaselementary","douglashigh","douglasmiddle","dreamjob411","dsviewer","e2010","ebes","ebooks","eclass","eclass2","ecsinow","ecspowerschool","edulog","edutrax","ees","eforms","email","employeeportal","engage","engage2","engagepd","es","eschool","eschoolhac","esmoodle","esms","ess","et","etcentral","etcontent","etsecurity","etsts","eurabrown","evans","excert","exchange","expressway","faine","fairview","falcon1","familylink","fce","fed","fes","filewave","filter","finance","floyd","formcentral","forms","fortis","frame","franklin","fs","ftp","gadsdencity-hs","gchs","girard","girardms","gmail","gms","gpa","grandview","greene","grpwise","guac","guac-test","gwguard","happytimes","hcs-ess","hct","hd","hdcsmtp1","hdctab","heard","helpdesk","henryclay","henryconnects","heritagehigh","hes","hhs","highlands","hms","homewood","honeysuckle","hs","iboss","ibossoc","ibossreporter","icreports","imail","info","infocus","infonowweb","inow","inowapi","inowhome","inowreports","inowtest","interweb","intranet","inventory","it","jasper","jds","join","jrotc1","jsj-cam","jupiter","kb","kbox","kc","kellysprings","keynet","kronmobile","kronos","lcs-amid01","ldap","lee","les","lesmoodle","lessonplans","lhs","lhsmoodle","lib","library","lightspeed","lightspeed2","links","listsrv","lms","maconexch","madisoncity","mahara","mail","mail1","mail2","mail4","mail7","mailserver","maintenance","maps","marengo","matterhorn","mbsasa","mc","mcep","mconline","mcpsnet","mcs-tools","mdm","mdm2","mealapplication","mealapps","media","meet","mes","mesmoodle","mhsmoodle","midfield","mine","mitchell","mmsmoodle","mobile","mobilefilter","monroe","montage","montagebeta","montana","moodle","moodle17","mps","mps-filewave","mps-powerschool","mps-rdp-01","mps-solarwinds","msc-mobile","msc-print","msc7","mscs","mserve","mta","mta-sts","mts","mx","mx1","my","mydocs","myfiles","mypay","mystop","mytime","n2h2","nagios","nas","netview","newmail","nextgen","ng","ngweb","nms","northview","ns","ns1","ns2","nutrition","oaes","ocsad3","ocsarchive","ocsbo","ocscomm","ocsgwava","ocshelpdesk","ocslms","ocsmail","ocsweb","ocswww","odyssey","oldmail","oldregistration","onlinemealapp","opelika-ls","owa","packetview","pandora","paperless","parent","parentportal","parentsurvey","passwordreset","passwordresetregistration","patriotpath","payday","paydocs","payroll","paystubs","pbx","pcmon","pcslibrary","pd","pdexpress","pdmoodle","piedmont","pinpoint","podcasts","pop","portal","powerschool","pres","preschool","proxy","proxy2","ps-sandbox","ps-test","pssb","pwchange","quarantine","radius","randolph","rbhudson","rcs","rdp","rds","read","readydesk","registration","relay","remotesupport","renlearn","reporter","request","res","reset","roatws1","rocket","rollcall","router","rp","rpad","rsapi","rta-app-a","rta-app-b","s","safari","safariaves","schools","score","scripting","scs","scsinfnow","scsmail","scsnxgnsvc","search","searchsoft","searchsoftauth","secure","securelink","security","securityportal","sedna","selmast","services","ses","sesmoodle","sets","setshome","setsser","setsti","setsweb","sftp","shelbyed","showcase","shssec","sis","sjhs","slingluff","slomanprimary","sms","smtp","smtp-1","smtp1","smtp11","smtp2","sonicwallva","sophos","spam","spam2","spamtitan1","spamtitan2","spc","specialty","sresmoodle","sso","sspr","staffportal","staffsurvey","status","sti","stidistrict","stisets","stisetsweb","striplin","sts","studentportal","subfinder","subportal","sumter","support","supportportal","swinstall","synergy","synergypsv","sysaid","tarrant","tcchsmoodle","tcs-docs","tcsd-ns-01","tcsd-ns-02","tcsdns","tcsfirewall","tcsscobia","teacherportal","technology","techweb","techwiki","temp","temptrak","tes","test","test5","testps","thompson","ths","tickets","timeclock","tm","tools","transelog","transportation","trend","tserver","ttc-smb","ttc-spam","turn","tuscumbia","ugms","uniongrove","updates","utm","view","view1","view2","voip-expressway-e","vpec01","vpn","walnutpark","wayfinder","wb","wboesfb","web","webcentral","webcrd","webdisk","webmail","webmail2","websets","wes","wesmoodle","wessec","whsmoodle","wiki","wilcox","williamblount","winfield","workorder","workorders","wpes","www","www1","www2","wx"]
    subdomains = random.sample(subdomains,len(subdomains))
    for _ in subdomains:
        success = False

        if _ == "":
            dns_host = host
        else:
            dns_host = f"{_}.{host}"

        # check reverse dns
        print(CYAN + f"checking for reverse dns on {dns_host}")
        time.sleep(delay)
        try:
            hits.append(f"reverse dns {dns_host}: {socket.gethostbyaddr(dns_host)}")
            success = True
        except:
            pass
        # check if host is up
        print(CYAN + f"checking {dns_host}")
        time.sleep(delay)
        try:
            my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            my_socket.settimeout(1.25)
            my_socket.connect((dns_host,80))
            my_socket.close()
            hits.append(f"found {dns_host}")
            success = True
        except ConnectionRefusedError:
            hits.append(f"found {dns_host}")
            success = True
        except socket.timeout:
            hits.append(f"found {dns_host}")
            success = True
        except:
            pass

        if success:
            # check ssl certification info
            print(CYAN + f"checking ssl cert on: {dns_host}")
            time.sleep(delay)
            try:
                context = ssl.create_default_context()
                context.check_hostname = True
                ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=dns_host)
                ssl_socket.settimeout(10)
                ssl_socket.connect((dns_host,443))
                data = ssl_socket.getpeercert()
                ssl_socket.close()
                cert = data["serialNumber"]
                hits.append(f"ssl serial number {dns_host}: {data['serialNumber']}")
                hits.append(f"ssl expires {dns_host}: {data['notAfter']}")
            except:
                pass
            time.sleep(delay)
            try:
                context = ssl.create_default_context()
                context.check_hostname = True
                ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=dns_host)
                ssl_socket.settimeout(10)
                ssl_socket.connect((dns_host,8443))
                data = ssl_socket.getpeercert()
                ssl_socket.close()
                cert = data["serialNumber"]
                hits.append(f"ssl serial number {dns_host}: {data['serialNumber']}")
                hits.append(f"ssl expires {dns_host}: {data['notAfter']}")
            except:
                pass

    clear()
    hits.sort()
    for hit in hits:
        print(CYAN + hit)

    with open(f"{host}.txt","a") as file:
        for hit in hits:
            file.write(f"{hit}\n")

    print(CYAN + f"{len(hits)} results")
