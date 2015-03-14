from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
from classic_models.models import CustomerGroup, GroupList,customers,Campaigns,CampaignForGroup,campaign_targetgroup_players,campaigns_dps,campaigns_for_groups,daily_player_summary
import MySQLdb
import datetime
import time
from datetime import timedelta
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from highcharts.views import HighChartsBarView
@csrf_exempt
def groups(request):
    
    groups=CustomerGroup.objects.all()
    group_list = GroupList()
    all={}
    template = loader.get_template('classic_models/groups.html')
    context = RequestContext(request)
    group_name=""
    
    if request.method == "POST":
        sel_group_id=request.POST.get("groups")
        if sel_group_id:
            groups=CustomerGroup.objects.all()
            groups=groups.filter(groupID__exact=sel_group_id)
            for g in groups:
                cities_send=g.city
                countries_send=g.country
                credit_send=g.creditLimit
                emp_send=g.salesRepEmployeeNumber
                grp_name_send=g.groupName

                if cities_send:
                    all['cities_send']=cities_send.split(",")
                if countries_send:
                    all['countries_send']=countries_send.split(",")
                if credit_send>0:
                    all['credit_send']=int(credit_send)
                if emp_send:
                    all['emp_no_send']=emp_send.split(",")
                all['grp_name']=grp_name_send
                all['grp_id']=sel_group_id
            groups=CustomerGroup.objects.all()
            all['group']=groups
            return render_to_response('classic_models/groups.html',all)
        
        cities_names=request.POST.get("cities")
        country_names=request.POST.get("countries")
        creditlimits=request.POST.get("creditlimits")
        empNos=request.POST.get("empNos")

        li_city=[]
        li_country=[]
        li_creditlimit=0
        li_empno=[]
        cities_names=cities_names[1:]
        country_names=country_names[1:]
        empNos=empNos[1:]

        if len(cities_names)>0:
            li_city = cities_names.split(",")
        if len(country_names)>0:
            li_country = country_names.split(",")
        li_creditlimit = creditlimits
        if len(empNos)>0:
            li_empno = empNos.split(",")
         
        group_name=request.POST.get("group_name","")
        groupid=request.POST.get("groupid","")

        if len(groupid)>0:
            group = CustomerGroup.objects.get(groupID=groupid)            
        else:
            group= CustomerGroup()
        groups1=customers.objects.all()
        group.groupName = group_name
        if len(li_city)>0:
            groups1=groups1.filter(city__in=set(li_city))
            group.city = ','.join(set(li_city))
        if len(li_country)>0:
            groups1=groups1.filter(country__in=set(li_country))
            group.country = ','.join(set(li_country))
        if li_creditlimit>0:
            groups1=groups1.filter(creditLimit__gte=li_creditlimit)
            group.creditLimit = Decimal(li_creditlimit)
        if len(li_empno)>0:
            groups1=groups1.filter(salesRepEmployeeNumber__in=set(li_empno))   
            group.salesRepEmployeeNumber=','.join(set(li_empno))
        cust_id="" 
        for c in groups1:
            cust_id+=','+str(c.customerNumber)
       # import pdb;pdb.set_trace()
        group.save()

        if len(groupid)>0:
            group_list = GroupList.objects.get(group_id=groupid)            
        else:
            group_list.group_id = group
        
        group_list.customer_id = cust_id[1:]
        group_list.save()
        
    groups=CustomerGroup.objects.all()
    group_list = GroupList()
    all={}  
    all['group']=groups
    return render_to_response('classic_models/groups.html',all)

@csrf_exempt
def campaigns(request):
    template = loader.get_template('classic_models/campaigns.html')
    context = RequestContext(request)
    all={}
    if request.method == "POST":
        sel_campaign_id=request.POST.get("campaigns")
        if sel_campaign_id:
            campaign=Campaigns.objects.all()
            campaign=campaign.filter(campaignID__exact=sel_campaign_id)
            campaignsforgroup=CampaignForGroup.objects.all()
            campaignsforgroup=campaignsforgroup.filter(campaignID__exact=sel_campaign_id)
            all['groups_send']=campaignsforgroup
            for c in campaign:
                all['camp_name']=c.campaignName
            all['camp_id']=sel_campaign_id
            groups=CustomerGroup.objects.all()
            group4=Campaigns.objects.all()
            print groups
            all['campaigns']=group4
            all['group']=groups
            return render_to_response('classic_models/campaigns.html',all)
        groups_names=request.POST.get("groups")
        dates_names=request.POST.get("dates")
        

        li_group=[]
        li_date=[]
        groups_names=groups_names[1:]
        dates_names=dates_names[1:]

        if len(groups_names)>0:
            li_group = groups_names.split(",")
        if len(dates_names)>0:
            li_date = dates_names.split(",")
         
        camp_name=request.POST.get("campaign_name","")
        campid=request.POST.get("campid","")
        
        
        if len(campid)>0:
            campaign= Campaigns.objects.get(campaignID=campid)            
        else:
            campaign= Campaigns()
        campaign.campaignName=camp_name
        campaign.save()
        
        i=0
        
        if len(campid)>0:
            CampaignForGroup.objects.filter(campaignID=campid).delete()
        
        while i<len(li_group):            
            campforgrp = CampaignForGroup()
            campforgrp.campaignID= campaign
            campforgrp.startDate=datetime.datetime.strptime(li_date[i], '%Y-%m-%d').date()
            campforgrp.groupID=int(li_group[i])
            campforgrp.save()
            i=i+1
    groups=CustomerGroup.objects.all()
    group4=Campaigns.objects.all()
    all={}
    all['campaigns']=group4
    all['group']=groups
    return render_to_response('classic_models/campaigns.html',all)

@csrf_exempt
def view_schedule(request):
    template = loader.get_template('classic_models/view_schedule.html')
    context = RequestContext(request)
    print request.method
    all={}
    li=[]
    z = 0
    if request.method == "POST":
        day=request.POST.get("dates")
    else:
        day=time.strftime("%Y-%m-%d")
    print day
    dt = datetime.datetime.strptime(day, '%Y-%m-%d').date()
    start_date = dt - timedelta(days = (dt.weekday()+1)%7)
    end_date = start_date + datetime.timedelta(days=6)
    print start_date
    print end_date
    campaign_groups=CampaignForGroup.objects.all()
    groups=CustomerGroup.objects.all()
    campaigns=Campaigns.objects.all()
    campaign_groups=campaign_groups.filter(startDate__range=(start_date,end_date))
    dict={}
    dict1={}
    for g in campaign_groups:
        group_name=""
        camp1=[]
        group_name=str(groups.get(groupID__exact=g.groupID).groupName)
        dt1=(g.startDate)
        camps=str(g.campaignID.campaignName)
        cc=CampaignForGroup.objects.filter(groupID__exact=g.groupID,startDate__exact=g.startDate)
        #dict.setdefault(group_name, {})[dt1]=camps
        dict.setdefault(group_name,[]).append(dt1)
    print dict
    for k,v in dict.items():
        gid=groups.get(groupName__exact=k).groupID
        #print gid
        print v
        for i in v:
            cc=CampaignForGroup.objects.filter(groupID__exact=gid,startDate__exact=i)
            camps=[]
            for d in cc:
                camps.append(str(d.campaignID.campaignName))
                dict1.setdefault(k, {})[i]=camps
    print dict1      
    #print dict
    all['start_date']=start_date
    all['dic']=dict1
    all['date1']=day
    d=start_date
    while d<=end_date:
         li.append(d);
         d=d+ datetime.timedelta(days=1)
    print li
    all['aa']=li
    return render_to_response('classic_models/view_schedule.html',all)

@csrf_exempt
def Dashboard(request):
    template = loader.get_template('classic_models/Dashboard.html')
    groups=campaigns_for_groups.objects.all()
    groups1=campaigns_dps.objects.all()
    all={}
    all['date']=groups
    all['camp_name']=groups1
    db = MySQLdb.connect("10.0.0.109","classicmodels","classicmodels","classicmodels_django" )
    cursor = db.cursor()
    cursor1 = db.cursor()
    cursor2 = db.cursor()
    cursor.execute("SELECT ctp.target_control_cd, COUNT(DISTINCT ctp.wh_player_id) group_size, COUNT(DISTINCT CASE WHEN dps.deposit_amt > 0 THEN dps.wh_player_id END) depositing_player_size, COUNT(DISTINCT CASE WHEN dps.trx_ggr_amt > 0 THEN dps.wh_player_id END) ggr_player_size, SUM(deposit_amt) total_deposit_amt, AVG(deposit_amt) avg_deposit_amt, SUM(trx_ggr_amt) trx_ggr_amt, AVG(trx_ggr_amt) avg_ggr_amt FROM campaign_targetgroup_players ctp LEFT JOIN daily_player_summary dps ON ctp.wh_player_id = dps.wh_player_id AND dps.summary_date BETWEEN '2014-07-01' AND '2014-07-07' AND ctp.campaign_Code = 'C1' AND ctp.target_Group = 'TG1' GROUP BY 1")
    data = cursor.fetchall()
    cursor1.execute("select ctp.wh_player_id, sum(deposit_amt) deposits, sum(trx_ggr_amt) net_ggr from campaign_targetgroup_players ctp left join daily_player_summary dps on ctp.wh_player_id = dps.wh_player_id and dps.summary_date between '2014-07-01' and '2014-07-07' and ctp.campaign_Code = 'C1' and ctp.target_Group = 'TG1' and ctp.target_control_cd = 'T' group by 1 having sum(Deposit_amt) > 0")
    data1 = cursor1.fetchall()
    cursor2.execute("SELECT target_control_Cd,summary_date,(CASE WHEN target_control_Cd = 'T' THEN @csum2:= @csum2 + depositing_player_size ELSE @csum3:= @csum3 + depositing_player_size END) AS cc_dep,(CASE WHEN target_control_Cd = 'T' THEN (@csum:= @csum + depositing_player_size) / @tarsize ELSE (@csum1:= @csum1 + depositing_player_size) / @tarsize END)*100 AS cum_dep,(CASE WHEN target_control_Cd = 'T' THEN @csum2:= @csum2 + ggr_player_size ELSE @csum3:= @csum3 + ggr_player_size END) AS cc_ggr,(CASE WHEN target_control_Cd = 'T' THEN (@csum:= @csum + ggr_player_size) / @tarsize ELSE (@csum1:= @csum1 + ggr_player_size) / @tarsize END)*100 AS cum_ggr FROM (SELECT a.target_control_Cd,a.summary_date,b.group_size, a.depositing_player_size,a.ggr_player_size FROM (SELECT ctp.target_control_cd, dps.summary_date, COUNT(DISTINCT CASE WHEN dps.deposit_amt > 0 THEN dps.wh_player_id END) depositing_player_size, COUNT(DISTINCT CASE WHEN dps.trx_ggr_amt > 0 THEN dps.wh_player_id END) ggr_player_size FROM campaign_targetgroup_players ctp JOIN daily_player_summary dps ON ctp.wh_player_id = dps.wh_player_id AND dps.summary_date BETWEEN '2014-07-01' AND '2014-07-07' AND ctp.campaign_Code = 'C1' AND ctp.target_Group = 'TG1' GROUP BY 1,2 ORDER BY 1,2) a,(SELECT ctp.target_control_cd, COUNT(1) group_size FROM campaign_targetgroup_players ctp GROUP BY 1 ORDER BY 1) b WHERE a.target_control_cd = b.target_control_cd GROUP BY 1,2 ORDER BY 1,2) gr JOIN (SELECT @csum:= 0) c JOIN (SELECT @csum1:= 0) d JOIN (SELECT @csum2:= 0) e JOIN (SELECT @csum3:= 0) h JOIN (SELECT @tarsize:= COUNT(*) FROM campaign_targetgroup_players) f ORDER BY 1,2")
    data2 = cursor2.fetchall()
    ctrl_groupsize=0
    trgt_groupsize=0
    ctrl_playersize=0
    trgt_playersize=0
    ctrl_perc=0.0
    trgt_perc=0.0
    ctrl_avgdeposit=0
    trgt_avgdeposit=0
    ggrctrl_playersize=0
    ggrtrgt_playersize=0
    ggrctrl_perc=0.0
    ggrtrgt_perc=0.0
    ggrctrl_avgdeposit=0
    ggrtrgt_avgdeposit=0
    
    for e in data: 
        if e[0]=='C':
            ctrl_groupsize=e[1]
            ctrl_playersize=e[2]
            ctrl_avgdeposit=round(e[5],2)
            ggrctrl_playersize=e[3]
            ggrctrl_avgdeposit=e[7]
        else:
            trgt_groupsize=e[1]
            trgt_playersize=e[2]
            trgt_avgdeposit=round(e[5],2)
            ggrtrgt_playersize=e[3]
            ggrtrgt_avgdeposit=e[7]
    ctrl_perc=round((float(ctrl_playersize*100))/(ctrl_playersize+trgt_playersize),2)
    trgt_perc=100-ctrl_perc
    ggrctrl_perc=round((float(ggrctrl_playersize*100))/(ggrctrl_playersize+ggrtrgt_playersize),2)
    ggrtrgt_perc=100-ggrctrl_perc
    all['controlgroupsize']=ctrl_groupsize
    all['targetgroupsize']=trgt_groupsize
    all['controlplayersize']=ctrl_playersize
    all['targetplayersize']=trgt_playersize
    all['controlpercentage']=ctrl_perc
    all['targetpercentage']=trgt_perc
    all['controlavgdeposit']=ctrl_avgdeposit
    all['targetavgdeposit']=trgt_avgdeposit
    all['ggrcontrolplayersize']=ggrctrl_playersize
    all['ggrtargetplayersize']=ggrtrgt_playersize
    all['ggrcontrolpercentage']=ggrctrl_perc
    all['ggrtargetpercentage']=ggrtrgt_perc
    all['ggrcontrolavgdeposit']=ggrctrl_avgdeposit
    all['ggrtargetavgdeposit']=ggrtrgt_avgdeposit
    
    
    wh_player_id=[]
    all['playerid']=data1
    
    date_graph=[]
    ctrl_graph=[]
    trgt_graph=[]
    for e in data2:
        if e[0]=='C':
            date_graph.append(e[1])
            ctrl_graph.append(round(e[3],2))
        else:
            trgt_graph.append(round(e[3],2))
    #date_graph=set(date_graph)
    print date_graph
    print ctrl_graph
    print trgt_graph
    all['dategraph']=date_graph
    all['controlgraph']=ctrl_graph
    all['targetgraph']=trgt_graph
    
    return render_to_response('classic_models/Dashboard.html',all)

@csrf_exempt
def home(request):
    template = loader.get_template('classic_models/home.html')
    return render_to_response('classic_models/home.html',all)
    
