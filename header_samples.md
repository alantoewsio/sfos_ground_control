# Header Samples

## Pre-Login

### ::1:: GET /webconsole/webpages/login.jsp HTTP/1.1

#### Request headers (login.jsp)

``` raw headers
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Cache-Control: max-age=0
Connection: keep-alive
Cookie: JSESSIONID=161pmgkuzi9s4yv8nkfgrjat177813; wfx_unq=7tNYD7LafL4ANyOm
DNT: 1
Host: boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/index.jsp
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

#### Request body (login.jsp)

``` raw request body
<empty>
```

#### Response headers (login.jsp)

``` raw headers
Cache-Control: no-cache
Connection: close
Content-Length: 6391
Content-Security-Policy: default-src https: data: ws: wss: blob: 'unsafe-inline' 'unsafe-eval'; worker-src 'self' blob:; frame-ancestors self';
Content-Type: text/html;charset=utf-8
Date: Mon, 03 Jun 2024 15:20:59 GMT
Expires: Wed, 31 Dec 1969 23:59:59 GMT
Pragma: no-cache
Server: xxxx
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-Xss-Protection: 1; mode=block
```

## Login

### ::2:: POST /webconsole/Controller HTTP/1.1

#### Request headers (Controller login)

``` raw headers
Accept: text/plain, */*; q=0.01
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Content-Length: 185
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: JSESSIONID=161pmgkuzi9s4yv8nkfgrjat177813; wfx_unq=7tNYD7LafL4ANyOm
DNT: 1
Host: boston.toews.io:4444
Origin: https://boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/login.jsp
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
X-Requested-With: XMLHttpRequest
sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

#### Raw request body (Controller login)

``` raw body
mode=151&json=%7B%22username%22%3A%22admin%22%2C%22password%22%3A%22Sophos%3D111%22%2C%22languageid%22%3A%221%22%2C%22browser%22%3A%22Chrome_125%22%7D&__RequestType=ajax&t=1717428049511
```

#### Parsed request body (Controller login)

``` parsed body
mode: 151
json: {"username":"admin","password":"Sophos=111","languageid":"1","browser":"Chrome_125"}
__RequestType: ajax
t: 1717428049511
```

#### Response headers (Controller login)

``` raw headers
HTTP/1.1 200 OK
Date: Mon, 03 Jun 2024 15:21:08 GMT
Server: xxxx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Content-Type: text/plain;charset=iso-8859-1
Expires: Thu, 01 Jan 1970 00:00:00 GMT
Content-Length: 53
Set-Cookie: JSESSIONID=yrlybf54kw8zv264lzltyq7v177814; Path=/webconsole; Secure; HttpOnly
Connection: close
```

#### Response body (Controller login)

``` raw response
<empty>
status codes
200=success
```

### ::3:: GET /webconsole/webpages/index.jsp HTTP/1.1

#### Request Headers (index.jsp)

``` raw headers
GET /webconsole/webpages/index.jsp HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Cookie: JSESSIONID=yrlybf54kw8zv264lzltyq7v177814; wfx_unq=7tNYD7LafL4ANyOm
DNT: 1
Host: boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/login.jsp
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

#### Response headers (index.jsp)

``` raw headers
HTTP/1.1 200 OK
Date: Mon, 03 Jun 2024 15:21:09 GMT
Server: xxxx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Content-Security-Policy: default-src https: data: ws: wss: blob: 'unsafe-inline' 'unsafe-eval'; worker-src 'self' blob:; frame-ancestors 'self';
X-XSS-Protection: 1; mode=block
Content-Type: text/html;charset=utf-8
Cache-Control: no-store
Pragma: no-cache
Expires: Wed, 31 Dec 1969 23:59:59 GMT
Connection: close
Transfer-Encoding: chunked
```

#### Response body (index.jsp)

``` html
<!DOCTYPE HTML>
--104 blank lines removed--
<html>
<head>
<title>boston.toews.io</title>
--44 blank lines removed--
<script>
	var objectID = 0;
	var uiLangToHTMLLangAttributeValueMapping={"English":"en","Chinese-Traditional":"zh-Hant","Chinese-Simplified":"zh-Hans","French":"fr",
		"Japanese":"ja","Italian":"it","Korean":"ko","Brazilian-Portuguese":"pt","Russian":"ru","Spanish":"es","German":"de"};
	var selectedLang='English';
	document.getElementsByTagName("html")[0].setAttribute("lang",uiLangToHTMLLangAttributeValueMapping[selectedLang]);
</script>
-- 5 blank lines--
<link href="/iview/lite1css/container.css?version=077b68eec97ffaa545be811dc65cee99" rel="stylesheet" type="text/css" />
<link rel="stylesheet" href="/iview/lite1css/reports.css?version=077b68eec97ffaa545be811dc65cee99">
<LINK REL="ICON" HREF="/images/favicon.ico?version=077b68eec97ffaa545be811dc65cee99">
<link href="/themes/lite1/css/typography.css?version=077b68eec97ffaa545be811dc65cee99" rel="stylesheet" type="text/css" />
<link href="/themes/lite1/css/font-awesome.css?version=077b68eec97ffaa545be811dc65cee99" rel="stylesheet" type="text/css" />
<link href="/themes/lite1/css/icomoon.css?version=077b68eec97ffaa545be811dc65cee99" rel="stylesheet" type="text/css" />
<link href="/themes/lite1/css/Sophos-Icons.css?version=077b68eec97ffaa545be811dc65cee99" rel="stylesheet" type="text/css" />
<link href="/themes/lite1/css/common_min.css?version=077b68eec97ffaa545be811dc65cee99" rel="stylesheet" type="text/css" />
<link href="/themes/lite1/css/control-center.css?version=077b68eec97ffaa545be811dc65cee99" rel="stylesheet" type="text/css" />
<link href="/css/passwordStrength.css?v=077b68eec97ffaa545be811dc65cee99" rel="stylesheet" type="text/css" />
<link href="/css/passwordStrengthMeter.css?v=077b68eec97ffaa545be811dc65cee99" rel="stylesheet" type="text/css" />
</head>
<body class="indexbody yui-skin-sam" scrolling="no" id="mainbody">
  <div id="wrapper" class="cp-wrapper">
    <section class="left-pnl">
      <div id="logo-container"><a href="index.jsp"><img id="sophos-logo" class="" src="/images/logo/logo.png?v=077b68eec97ffaa545be811dc65cee99" /></a>
      </div>
      
	  <div id="menu-search-container"></div>
	  <div id="left-menu-container"></div>
    </section>
    <section id="body" class="right-pnl wrapper">
	  <div id="topbar" style="display:table;box-sizing:border-box;padding:0 10px;">
		<div style="margin-left: -10px;">
				<div id="eap-banner"></div>
				<div id="top-central-banner"></div>
				<div id="auxiliary-banner"></div>
				<div id="top-npu-banner"></div>
				<div id="top-raid-banner"></div>
		</div>
		<div id="topbar-title" style="display:inline-block;vertical-align:middle;">
		<div id="breadcrumbs" class="breadcrumbs"></div>
		</div>
		<div id="top-right-menu" style="display:inline-block;vertical-align:middle;text-align:right;">
		<div style="display:table;float:right;">
				<div id="acc-icon" style="display:table-cell;float:right;padding:0px 0px 0px 5px;">
					<div id="acc-btn"></div>
				</div>
	        	<div id="help-btn" style="display:none;float:right;padding:0px 12px 0px 5px;" onclick="openHelp();">
					<a><label id="Language.Help" style="cursor:pointer;"></label></a>
				</div>
				<div id="log-btn" style="display:table-cell;float:right;padding:0px 12px 0px 5px;" onclick="openLogviewer();">
					<a><label id="Language.LogViewer" style="cursor:pointer;"></label></a>
				</div>
				<div id="hwto-add" style="display:none;float:right;padding:0px 12px 0px 5px;">
					<a id="howToVideosHref" target="_blank"><i class="fa fa-video-camera" aria-hidden="true"></i><label id="Language.HowToGuides" style="cursor:pointer;padding-left:5px;"></label></a>
				</div>
				
					<div id="feedback" style="display:table-cell;float:right;padding:0px 12px 0px 5px;">
						<a id="feedbackhref" onClick="openUserSnapWidget()"><label id="Language.Feedback" style="cursor:pointer;padding-left:5px;"></label></a>
					</div>
				
			</div>
			<div style="display:table;width:100%;">
				<span style="font-size: 12px; float: right;padding-right: 3px;">Sophos Ltd</span>
			</div>
    	</div>
    	<div id="main-tab-container"></div>
      </div>
      <div id="mainframediv" class="mainframecontent" style="overflow: auto;">
        <div id="inlinePopup"></div>
		<div id="mainframecontent"></div>
      </div>
      <div class="statusbar" id="mystatusbar" onmouseover="Cyberoam.statusbarOver()" onmouseout="Cyberoam.statusbarOut()"></div>
    </section>
  </div>
<script type="text/javascript" src="/javascript/lang/English/common.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/javascript/lang/English/OEM.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/iview/javascript/lang/English/report.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/iview/javascript/lang/English/report_extra.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/javascript/jQueryYUI.js?v=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/javascript/validation/JavaConstants.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/javascript/validation/OEM.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/javascript/react-0.12.2/react.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/javascript/common_min.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/javascript/eventstatus.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/themes/lite1/javascript/theme.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/javascript/lang/English/calendar-lang.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/javascript/react-components/menu-data.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/javascript/password_strength_lightweight.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/javascript/globalSearchService.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/javascript/entity-map.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<!-- Iview Code -->
<script type="text/javascript" src="/iview/FusionCharts/fusioncharts.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/iview/FusionCharts/fusioncharts.charts.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/iview/javascript/countryinfo.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript" src="/iview/javascript/common_pdfmake.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<!-- Iview Code -->
<script type="text/javascript">
	$(document).ready(function() {
		$("#wrapper").width($(window).width());
		$(window).on('resize',function() {
			$("#wrapper").width($(window).width());
		});
	
		displayEapBanner();
		if(isNPUfailed){
			NPUDisplayBanner();
		}else if(isFaultyDisk){
			RaidDisplayBanner();
		} else {
			cm2DisplayBanner();
		}
		//calling functionn for aux banner
		displayAuxBanner();
		fetchHAInfo();
	});
	Cyberoam.c$rFt0k3n = 'mfd4du0g7dnmvmb5pa8assf1bp';
	Cyberoam.setCSRFToken(Cyberoam.c$rFt0k3n);
	Cyberoam.images = "themes/lite1/images";
	Cyberoam.language = "English";
	Cyberoam.isCentralLogin = JSON.parse("false");
	Cyberoam.displayModel = 'XGS2300';
	Cyberoam.applianceGroup = 'NONE';
	Cyberoam.displayVersion = 'SFOS 20.0.0 GA-Build222';
	Cyberoam.applianceKey = 'X23001RQQV66831';
	Cyberoam.firmwareVersionOrgFormat = '20.0.0.222'
	Cyberoam.isOEMdevice = 'false';
	Cyberoam.version = "20.0.0.222";
	Cyberoam.loginUserName = "admin";
	Cyberoam.name = "admin";
	Cyberoam.companyName = "Sophos Ltd";
	Cyberoam.disableAdmin = "";
	Cyberoam.page = "";
	Cyberoam.isCCC = false;
	Cyberoam.actionURL = Cyberoam.contextPath+"/Controller";
	Cyberoam.deviceProperty = JSON.parse('{"maxsslvpnprocesses":"2","AVELITECOREMIRROR":"off","HBVersion":"4","ctrprocessfilepath":"/sdisk/ctr/","smtpscansize":"51200","heartbeatavailability":"1","mta_mode":"on","ipstimer_startDate":"0","is_sig_pkg_updated":"3","airgap_mode":"off","wirelessprotection":"on","domain_keyword_limit":"2000","redavailability":"1","reportfailreason":"0","mta":"enable","AMI":"off","popscansize":"10240","defaultinterfacespeed":"auto","optional_wifi":"off","file_upload_path":"/sdisk/upload","ipstimer_max":"30","ctrfilepath":"/sdisk/ctrfinal/","cccbackupfilepath":"/sdisk/conf/cccbackupdata/systemsnapshot","spamdigest":"on","LCD":"on","ftpscansize":"1572864","av_def_update":"on","SCFM_URL":"us-e1.cfm.sophos.com","gatewaycount":"1024","spx":"on","wlaniNG":"off","u2d_ips_dload_state":"success","sdwanprofilecount":"1024","av_sessions":"12","USBConfigImport":"0","XGS":"Profile1","atp_feature":"on","config maxsslsessions":"18432","dual_av":"1","config disable_hspcre":"0","airgap":"off","maxconnection":"3300","AVMIRRORDOMAIN":"avupdates.cyberoam.com","config maxappfilter":"127","config maxips":"127","waf":"on","max_open_sessions":"18432","max_user_cache_entries":"10000","vpn_low_enc":"off","icap_maxconnection":"32","var ssl_key_password":"nNX35CeHu5y4LFyP8EuYWkF","wlan_atheros9380":"off","dlp":"1","backupfilepath":"/sdisk/conf/backupdata/","logsandreports":"on","WPAx_Enterprise":"on","sslvpnpolicy":"on","wlan":"off","httpscansize":"1572864","icap":"off","ha":"on","quarantine":"on","ICVersion":"6"}');
	Cyberoam.internetSchemeCount = '0';
	Cyberoam.centralPromotionPopupState = "";
	var adminOperation=15;
	var loginUserSecurityLevel = 7;
	// var objectArray={};
	var isNPUfailed=false;
	var isFaultyDisk=false;
	var objectArray = {};
	Cyberoam.initMenuProperty();
	var logininwebconsol = 'yes';
	var wirelessLANING = Cyberoam.deviceProperty.wlaniNG;
	Cyberoam.IPv6Enable = 1;
	var modulesubsctionList=[{"is_bundle":"1","Status":"active","Type":"Eval","deactivation_reason":"","Start Date":"2020-12-14","Expiry Date":"2999-12-31","Name":"Base Firewall"},{"Status":"active","is_bundle":"1","deactivation_reason":"","Type":"Eval","Start Date":"2020-12-14","Expiry Date":"2999-12-31","Name":"Network Protection"},{"Status":"active","is_bundle":"1","deactivation_reason":"","Type":"Eval","Start Date":"2020-12-14","Expiry Date":"2999-12-31","Name":"Web Protection"},{"is_bundle":"0","Status":"active","Type":"Eval","deactivation_reason":"","Start Date":"2020-12-14","Expiry Date":"2999-12-31","Name":"Email Protection"},{"is_bundle":"0","Status":"active","Type":"Eval","deactivation_reason":"","Start Date":"2020-12-14","Expiry Date":"2999-12-31","Name":"Web Server Protection"},{"is_bundle":"1","Status":"active","Type":"Eval","deactivation_reason":"","Start Date":"2020-12-14","Expiry Date":"2999-12-31","Name":"ZeroDay Protection"},{"Status":"active","is_bundle":"1","deactivation_reason":"","Type":"Eval","Start Date":"2020-12-14","Expiry Date":"2999-12-31","Name":"Central Orchestration"},{"Status":"active","is_bundle":"1","deactivation_reason":"","Type":"Eval","Start Date":"2020-12-14","Expiry Date":"2999-12-31","Name":"Enhanced Support"},{"Status":"INACTIVE","is_bundle":"0","Type":"null","Start Date":"null","Expiry Date":"null","Name":"Enhanced Plus Support"},{"display_bundle":"Xstream Protection"}];
	var customerurl = 'http://customer.cyberoam.com/';
	// Admin password config for js
	Cyberoam.passwdComplexityChk = 0;
	Cyberoam.chkPasswdLength = 0;
	Cyberoam.passwdLength = 8;
	Cyberoam.upperLowerCase = 0;
	Cyberoam.numericCase = 0;
	Cyberoam.specialCase = 0;
	// Local user password config for js
	Cyberoam.userPasswdComplexityChk = 0;
	Cyberoam.chkUserPasswdLength = 0;
	Cyberoam.userPasswdLength = 8;
	Cyberoam.upperLowerCasePwForUser = 0;
	Cyberoam.numericCasePwForUser = 0;
	Cyberoam.specialCasePwForUser = 0;
	var countDownInterval = 120;
	var countDownTime=countDownInterval+1;
	var userRoleName='null';
	if(OEMProperty.howToVideoUrl && OEMProperty.howToVideoUrl != null){
		document.getElementById("howToVideosHref").href = OEMProperty.howToVideoUrl;
		document.getElementById("hwto-add").style.display = "table-cell";
	}
	if(OEMProperty.feature.onlineHelp){
		document.getElementById("help-btn").style.display = "table-cell";
	}
	function openCLIWindow() {
		var iMyWidth;
		var iMyHeight;
		//gets top and left positions based on user's resolution so hint window is centered.
		iMyWidth = (window.screen.width-875)/2;
		//half the screen width minus half the new window width (plus 5 pixel borders).
		iMyHeight = (window.screen.height-650)/2;
		//half the screen height minus half the new window height (plus title and status bars).
		var CLIwin = window.open("/webconsole/webpages/console.jsp?csrf=" + Cyberoam.c$rFt0k3n,'test',"status=yes, height=650,width=875,resizable=no,left=" + iMyWidth + ",top=" + iMyHeight + ",screenX=" + iMyWidth + ",screenY=" + iMyHeight + ",scrollbars=yes");
		CLIwin.focus();
	}
	function openWindow(){
		return;
		var iMyWidth;
		var iMyHeight;
		iMyWidth = (window.screen.width-900)/2;
		iMyHeight = (window.screen.height-590)/2;
		var win2 = window.open("/webconsole/webpages/wizard/mainpage.jsp?indexpage=yes",null,"status=yes, height=590,width=900,resizable=no,left=" + iMyWidth + ",top=" + iMyHeight + ",screenX=" + iMyWidth + ",screenY=" + iMyHeight);
		win2.focus();
		Cyberoam.setStatusBarMessage("","");
	}
	function openSupportPage(obj,url){
		obj.href = url;
		Cyberoam.setStatusBarMessage("","");
	}
	function openLogviewer(){
		Cyberoam.openLogViewerWindow();
	}
	function displayEapBanner() {
		var isEnabled = false;
		if (isEnabled
				&& sessionStorage.getItem("fw.eapBannerClosed") !== 'true') {
			React.render(React.createElement(Banner, {
				type : 'info',
				html : OEM.firewallEapBanner,
				closeable : true,
				onClose : function() {
					sessionStorage.setItem("fw.eapBannerClosed", "true");
					$("#eap-banner").hide();
				}
			}), $("#eap-banner")[0]);
			$("#eap-banner").show();
		} else {
			$("#eap-banner").hide();
		}
	}
	function displayAuxBanner(){
		//Showing Aux banner
		var query = "mode="+ Modes.GET_HA_TYPE+"&json={}";
		Cyberoam.AJAXCall({
			url:"/Controller?",
			dataType:"json",
			query: query,
			postResponse: function (data){
				var Device_HA_Type = data.HA_TYPE;
				AuxBanner(Device_HA_Type);
			}
		});
	}
	function AuxBanner(Device_HA_Type){
		if(Device_HA_Type == "Auxiliary"){
			if(sessionStorage.getItem("auxBanner") !== 'true') {
				React.render(React.createElement(Banner, {
					type : 'warn',
					html : Language.AuxiliaryBannerText,
					closeable : true,
					onClose : function() {
						sessionStorage.setItem("auxBanner", "true");
						$("#auxiliary-banner").hide();
					}
				}), $("#auxiliary-banner")[0]);
				$("#auxiliary-banner").show();
			}
		}else{
			$("#auxiliary-banner").hide();
		}
	}
	function cm2DisplayBanner() {
		var isEnabled = true;
		if (isEnabled && sessionStorage.getItem("CM2BannerClosed") !== 'true') {
			React.render(React.createElement(Banner, {
				type : 'error',
				text : Language.XGManagedByCentral,
				closeable : true,
				onClose : function() {
					sessionStorage.setItem("CM2BannerClosed", "true");
					$("#top-central-banner").hide();
				}
			}), $("#top-central-banner")[0]);
			$("#top-central-banner").show();
		}
		else {
			$("#top-central-banner").hide();
		}
	}
	function NPUDisplayBanner() {
		var npFailurePopupOpen = localStorage.getItem("NPUBannerClosed");
		npFailurePopupOpen=null;
		if (npFailurePopupOpen === null) {
			React.render(React.createElement(Banner, {
				type : 'error',
				text : Language.NPUStickyHeaderTitle,
				closeable : true,
				onClose : function() {
					sessionStorage.setItem("NPUBannerClosed", "true");
					$("#top-npu-banner").hide();
				}
			}), $("#top-npu-banner")[0]);
			$("#top-npu-banner").show();
		}
		else {
			$("#top-npu-banner").hide();
		}
	}
	function RaidDisplayBanner() {
		var raidFailurePopupOpen = localStorage.getItem("RaidBannerClosed");
		raidFailurePopupOpen=null;
		if (raidFailurePopupOpen === null) {
			React.render(React.createElement(Banner, {
				type : 'warn',
				html : Language.RaidDiskFailureLog,
				closeable : true,
				onClose : function() {
					sessionStorage.setItem("RaidBannerClosed", "true");
					$("#top-raid-banner").hide();
				}
			}), $("#top-raid-banner")[0]);
			$("#top-raid-banner").show();
		}
		else {
			$("#top-raid-banner").hide();
		}
	}
	function getHelpModule() {
		var module = Cyberoam.pageObject[Cyberoam.pageLayer].module;
		var i = 1;
		while (typeof module == "undefined") {
			if (Cyberoam.pageLayer - i < 0)
				return;
			module = Cyberoam.pageObject[Cyberoam.pageLayer - i].module;
			i++;
		}
		if (Cyberoam.getController() == "iview") {
			if (module == "report") {
				if (reportGroupList.config.type == "G") {
					module = "reportgroupid" + reportGroupList.config.reportGroup;
				} else {
					module = "reportid" + reportGroupList.config.report;
				}
			}
		} else {
			if (typeof Cyberoam.pageObject[Cyberoam.pageLayer].subModule != "undefined")
				module = module + "_" + Cyberoam.pageObject[Cyberoam.pageLayer].subModule;
		}
		return module;
	}
	function openHelpWindow(url, ver, lang, module, section, avoidCSRFInURL) {
		var mapObj = {
			"{version}": ver,
			"{lang}": lang,
			"{module}": module,
			"{section}": section,
		};
		url = url.replace(new RegExp("{version}|{lang}|{module}|{section}", "gi"), function (matched) {
			return mapObj[matched];
		});
		window.open(url, "_blank", "", avoidCSRFInURL);
	}
	function openHelp(module, section) {
		if (OEMProperty.feature.onlineHelp) {
			section = section || "";
			var lang = "English";
			var avoidCSRFInURL = true;
			var url = 'https://docs.sophos.com/nsg/sophos-firewall/{version}/Help/{lang}/webhelp/onlinehelp/index.html?contextID={module}#{section}';
			var appVersion = '20.0.0.222';
			var arrVerToken = appVersion.split(".");
			var helpVersion = arrVerToken[0] + "." + arrVerToken[1];
			var helpLang = ['de-de', 'ja-jp'];
			if ($.inArray(Cyberoam.languages[Cyberoam.language]["langTag"], helpLang) !== -1) {
				lang = Cyberoam.language;
			}
			if (url != '#') {
				module = module || getHelpModule();
				openHelpWindow(url, helpVersion, Cyberoam.languages[lang]["langTag"], module, section, avoidCSRFInURL);
			}
		}
	}
	function openLicensing(){
		menu.displayMenuByURL('/registration/ModuleLicense.jsp');
	}
	function validateMenuItem(module,aclEntity){
		if(typeof objectArray[module] != "undefined"){
			return false;
		}
		if(typeof aclEntity != "undefined" && (aclEntity == ACLEntityConstant.BACKUP || aclEntity == ACLEntityConstant.Restore)){
			if(typeof objectArray[ACLEntityConstant.BACKUP] != "undefined" && typeof objectArray[ACLEntityConstant.Restore] != "undefined")
				return false;
		}else if(typeof aclEntity != "undefined" && typeof objectArray[aclEntity] != "undefined"){
			return false;
		}
		return true;
	}
	if(document.getElementById("vrReports"))
		document.getElementById("vrReports").innerHTML = Language.Report;
	Cyberoam.setLabelValue();
	Cyberoam.setStatusBarMessage("","");
	Cyberoam.setPageSize();
	//MenuBar Rendering
	if (objectArray.hasOwnProperty('LOGSREPORTS')) {
		$(menuArr[0].childNodes[2]).splice(1,1);
	} else {
		menuArr[0].childNodes[2].childNodes=[{"appController":"iview","childNodes":[{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.TrafficDashboardDesc\"}","label":"reportlabels.Traffic_Dashboard","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Traffic_Dashboard","url":"report.html?action=1&json={reportgroupid:30}&empty=0,0,","reportgroupid":"30","tabtype":"general","groupjsonflag":"1","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.SecurityDashboardDesc\"}","label":"reportlabels.Security_Dashboard","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Security_Dashboard","url":"report.html?action=1&json={reportgroupid:40}&empty=0,1,","reportgroupid":"40","tabtype":"general","groupjsonflag":"1","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.ExecutiveReportDesc\"}","label":"reportlabels.Executive_Report","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Executive_Report","url":"report.html?action=1&json={reportgroupid:101}&empty=0,2,","reportgroupid":"101","tabtype":"general","groupjsonflag":"1","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.UserThreatQuotientDesc\"}","label":"reportlabels.User_Threat_Quotient_UTQ","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.User_Threat_Quotient_UTQ","url":"report.html?action=1&json={reportgroupid:1777010500}&empty=0,3,","reportgroupid":"1777010500","tabtype":"general","groupjsonflag":"1","displaytitle":"reportlabels.Reports","level3":"-1"}],"module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","label":"reportlabels.Dashboards","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Dashboards","url":"report.html?action=1&json={reportgroupid:30}&empty=0,","reportgroupid":"-1","tabtype":"general","groupjsonflag":"0","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","childNodes":[{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.UserAppRisksDesc\"}","label":"reportlabels.User_App_Risks___Usage","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.User_App_Risks___Usage","url":"report.html?action=1&json={reportgroupid:1999000010}&empty=1,0,","reportgroupid":"1999000010","tabtype":"general","groupjsonflag":"2","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","reportgroupid":"2110000030","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","label":"reportlabels.Cloud_Application_Usage","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","tabtype":"general","title":"reportlabels.Cloud Application Usage","groupjsonflag":"2","url":"report.html?action=1&json={reportgroupid:2110000030}&empty=1,1,","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.BlockedUserAppsDesc\"}","label":"reportlabels.Blocked_User_Apps","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.reportlabels.Blocked_User_Apps","url":"report.html?action=1&json={reportgroupid:1998000010}&empty=1,2,","reportgroupid":"1998000010","tabtype":"general","groupjsonflag":"2","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","reportgroupid":"1996000000","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.SynchronizedAppDesc\"}","label":"reportlabels.Synchronized_Applications","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","tabtype":"general","title":"reportlabels.Synchronized_Applications","groupjsonflag":"2","url":"report.html?action=1&json={reportgroupid:1996000000}&empty=1,3,","level3":"-1"},{"appController":"iview","reportgroupid":"-1","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","label":"reportlabels.Web","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","tabtype":"general","title":"reportlabels.Web","groupjsonflag":"0","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.WebRisksUsageDesc\"}","label":"reportlabels.Web_Risk___Usage","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Web_Risk___Usage","url":"report.html?action=1&json={reportgroupid:400000}&empty=1,5,","reportgroupid":"400000","tabtype":"general","groupjsonflag":"3","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","reportgroupid":"2110000050","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","label":"reportlabels.Web_Policy_Overrides","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","tabtype":"general","title":"reportlabels.Web Policy Overrides","groupjsonflag":"2","url":"report.html?action=1&json={reportgroupid:2110000050}&empty=1,6,","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.BlockedWebAttmptDesc\"}","label":"reportlabels.Blocked_Web_Attempts","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Blocked_Web_Attempts","url":"report.html?action=1&json={reportgroupid:800000}&empty=1,7,","reportgroupid":"800000","tabtype":"general","groupjsonflag":"3","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.SearchEngineDesc\"}","label":"reportlabels.Search_Engine","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Search_Engine","url":"report.html?action=1&json={reportgroupid:102000010}&empty=1,8,","reportgroupid":"102000010","tabtype":"general","groupjsonflag":"3","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","reportgroupid":"8800000","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","label":"reportlabels.Web_Content","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","tabtype":"general","title":"reportlabels.Web_Content_Filters","groupjsonflag":"3","url":"report.html?action=1&json={reportgroupid:8800000}&empty=1,9,","level3":"-1"},{"appController":"iview","reportgroupid":"-1","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","label":"reportlabels.Business_Applications","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","tabtype":"general","title":"reportlabels.Business_Applications","groupjsonflag":"0","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.WebServerUsageDesc\"}","label":"reportlabels.Web_Server_Usage","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Web_Server_Usage","url":"report.html?action=1&json={reportgroupid:1999000000}&empty=1,11,","reportgroupid":"1999000000","tabtype":"general","groupjsonflag":"4","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.WebServerprotectionDesc\"}","label":"reportlabels.Web_Server_Protection","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Web_Server_Protection","url":"report.html?action=1&json={reportgroupid:1888000000}&empty=1,12,","reportgroupid":"1888000000","tabtype":"general","groupjsonflag":"4","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","reportgroupid":"-1","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","label":"reportlabels.User_Data_Transfer","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","tabtype":"general","title":"reportlabels.User_Data_Transfer","groupjsonflag":"0","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.InternetUsageDesc\"}","label":"reportlabels.User_Data_Transfer_Report","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.User_Data_Transfer_Report","url":"report.html?action=1&json={reportgroupid:105000000}&empty=1,14,","reportgroupid":"105000000","tabtype":"general","groupjsonflag":"5","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","reportgroupid":"-1","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","label":"reportlabels.FTP","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","tabtype":"general","title":"reportlabels.FTP","groupjsonflag":"0","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.FTPUsageDesc\"}","label":"reportlabels.FTP_Usage","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.FTP_Usage","url":"report.html?action=1&json={reportgroupid:600000}&empty=1,16,","reportgroupid":"600000","tabtype":"general","groupjsonflag":"6","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.FTPProtectionDesc\"}","label":"reportlabels.FTP_Protection","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.FTP_Protection","url":"report.html?action=1&json={reportgroupid:1100000}&empty=1,17,","reportgroupid":"1100000","tabtype":"general","groupjsonflag":"6","displaytitle":"reportlabels.Reports","level3":"-1"}],"module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","label":"reportlabels.Application___Web","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Application___Web","url":"report.html?action=1&json={reportgroupid:1999000010}&empty=1,","reportgroupid":"-1","tabtype":"general","groupjsonflag":"0","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","childNodes":[{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.IntrusionAttacksDesc\"}","label":"reportlabels.Intrusion_Attacks","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Intrusion_Attacks","url":"report.html?action=1&json={reportgroupid:900000}&empty=2,0,","reportgroupid":"900000","tabtype":"general","groupjsonflag":"7","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.ATPDesc\"}","label":"reportlabels.Advanced_Threat_Protection","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Advanced_Threat_Protection","url":"report.html?action=1&json={reportgroupid:1666000070}&empty=2,1,","reportgroupid":"1666000070","tabtype":"general","groupjsonflag":"7","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.WirelessDesc\"}","label":"reportlabels.Wireless","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Wireless","url":"report.html?action=1&json={reportgroupid:40111000}&empty=2,2,","reportgroupid":"40111000","tabtype":"general","groupjsonflag":"7","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.SecurityHBDesc\"}","label":"reportlabels.Security_Heartbeat","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Security_Heartbeat","url":"report.html?action=1&json={reportgroupid:1699000010}&empty=2,3,","reportgroupid":"1699000010","tabtype":"general","groupjsonflag":"7","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","reportgroupid":"2100000010","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.SandBoxDesc\"}","label":"reportlabels.Zero_Day_Protection","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","tabtype":"general","title":"reportlabels.Zero_Day_Protection","groupjsonflag":"7","url":"report.html?action=1&json={reportgroupid:2100000010}&empty=2,4,","level3":"-1"}],"module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","label":"reportlabels.Network___Threats","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Network___Threats","url":"report.html?action=1&json={reportgroupid:900000}&empty=2,","reportgroupid":"-1","tabtype":"general","groupjsonflag":"0","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","childNodes":[{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.VPNDesc\"}","label":"reportlabels.VPN","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.VPN","url":"report.html?action=1&json={reportgroupid:200000010}&empty=3,0,","reportgroupid":"200000010","tabtype":"general","groupjsonflag":"14","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.SSLVPNDesc\"}","label":"reportlabels.SSL_VPN","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.SSL_VPN","url":"report.html?action=1&json={reportgroupid:200001001}&empty=3,1,","reportgroupid":"200001001","tabtype":"general","groupjsonflag":"14","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.ClientlessAccessDesc\"}","label":"reportlabels.Clientless_Access","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Clientless_Access","url":"report.html?action=1&json={reportgroupid:200000100}&empty=3,2,","reportgroupid":"200000100","tabtype":"general","groupjsonflag":"14","displaytitle":"reportlabels.Reports","level3":"-1"}],"module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","label":"reportlabels.VPN","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.VPN","url":"report.html?action=1&json={reportgroupid:200000010}&empty=3,","reportgroupid":"-1","tabtype":"general","groupjsonflag":"0","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","childNodes":[{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.EmailUsageDesc\"}","label":"reportlabels.Email_Usage","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Email_Usage","url":"report.html?action=1&json={reportgroupid:500000}&empty=4,0,","reportgroupid":"500000","tabtype":"general","groupjsonflag":"8","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.EmailProtectionDesc\"}","label":"reportlabels.Email_Protection","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Email_Protection","url":"report.html?action=1&json={reportgroupid:1000000}&empty=4,1,","reportgroupid":"1000000","tabtype":"general","groupjsonflag":"8","displaytitle":"reportlabels.Reports","level3":"-1"}],"module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","label":"reportlabels.Email","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Email","url":"report.html?action=1&json={reportgroupid:500000}&empty=4,","reportgroupid":"-1","tabtype":"general","groupjsonflag":"0","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","childNodes":[{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.HIPAADesc\"}","label":"reportlabels.HIPAA","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.HIPAA","url":"report.html?action=1&json={reportgroupid:2001}&empty=5,0,","reportgroupid":"2001","tabtype":"general","groupjsonflag":"9","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.GLBADesc\"}","label":"reportlabels.GLBA","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.GLBA","url":"report.html?action=1&json={reportgroupid:2002}&empty=5,1,","reportgroupid":"2002","tabtype":"general","groupjsonflag":"9","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.SOXDesc\"}","label":"reportlabels.SOX","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.SOX","url":"report.html?action=1&json={reportgroupid:2003}&empty=5,2,","reportgroupid":"2003","tabtype":"general","groupjsonflag":"9","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.FISMADesc\"}","label":"reportlabels.FISMA","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.FISMA","url":"report.html?action=1&json={reportgroupid:2005}&empty=5,3,","reportgroupid":"2005","tabtype":"general","groupjsonflag":"9","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.PCIDesc\"}","label":"reportlabels.PCI","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.PCI","url":"report.html?action=1&json={reportgroupid:2004}&empty=5,4,","reportgroupid":"2004","tabtype":"general","groupjsonflag":"9","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","iconCss":"","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.NERCCIPv3Desc\"}","label":"reportlabels.NERC_CIP_v3","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.NERC_CIP_v3","url":"report.html?action=1&json={reportgroupid:2040}&empty=5,5,","reportgroupid":"2040","tabtype":"general","groupjsonflag":"9","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","iconCss":"","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.CIPADesc\"}","label":"reportlabels.CIPA","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.CIPA","url":"report.html?action=1&json={reportgroupid:20051}&empty=5,6,","reportgroupid":"20051","tabtype":"general","groupjsonflag":"9","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.EventsDesc\"}","label":"reportlabels.Events","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Events","url":"report.html?action=1&json={reportgroupid:100000010}&empty=5,7,","reportgroupid":"100000010","tabtype":"general","groupjsonflag":"9","displaytitle":"reportlabels.Reports","level3":"-1"}],"module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","label":"reportlabels.Compliance","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Compliance","url":"report.html?action=1&json={reportgroupid:2001}&empty=5,","reportgroupid":"-1","tabtype":"general","groupjsonflag":"0","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","childNodes":[{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.CustomWebDesc\"}","label":"reportlabels.Custom_Web_Report","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Custom_Web_Report","url":"webusagesearch.html?action=4&groupjsonid=4&empty=6,0,","reportgroupid":"4","tabtype":"general","groupjsonflag":"22","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.CustomMailDesc\"}","label":"reportlabels.Custom_Mail_Report","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Custom_Mail_Report","url":"mailusagesearch.html?action=5&groupjsonid=5&empty=6,1,","reportgroupid":"5","tabtype":"general","groupjsonflag":"22","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.CustomFTPDesc\"}","label":"reportlabels.Custom_FTP_Report","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Custom_FTP_Report","url":"ftpusagesearch.html?action=8&groupjsonid=8&empty=6,2,","reportgroupid":"8","tabtype":"general","groupjsonflag":"22","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.CustomUserDesc\"}","label":"reportlabels.Custom_User_Report","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Custom_User_Report","url":"report.html?action=1&isCU=true&groupjsonid=26&json={reportgroupid:26}&empty=6,3,","reportgroupid":"26","tabtype":"general","groupjsonflag":"22","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.CustomWebServerDesc\"}","label":"reportlabels.Custom_Web_Server_Report","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Custom_Web_Server_Report","url":"wafusagesearch.html?action=115&groupjsonid=115&empty=6,4,","reportgroupid":"115","tabtype":"general","groupjsonflag":"22","displaytitle":"reportlabels.Reports","level3":"-1"}],"module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","label":"reportlabels.Custom","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Custom","url":"webusagesearch.html?action=4&groupjsonid=4&empty=6,","reportgroupid":"-1","tabtype":"general","groupjsonflag":"0","displaytitle":"reportlabels.Reports","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.CustomViewDesc\"}","label":"reportlabels.Custom_View","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Custom_View","url":"reportprofile.html?action=100&empty=7,","reportgroupid":"-1","tabtype":"setting","groupjsonflag":"0","displaytitle":"reportlabels.Report_Settings","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.ReportNotificationDesc\"}","label":"reportlabels.Report_Scheduling","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Report_Scheduling","url":"managemailschedule.html?action=80&empty=8,","reportgroupid":"-1","tabtype":"setting","groupjsonflag":"0","displaytitle":"reportlabels.Report_Settings","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.DataMgMtDesc\"}","label":"reportlabels.Data_Management","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Data_Management","url":"configdatabase.html?action=11&empty=9,","reportgroupid":"-1","tabtype":"setting","groupjsonflag":"0","displaytitle":"reportlabels.Report_Settings","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.ManualPurgeDesc\"}","label":"reportlabels.Manual_Purge","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Manual_Purge","url":"manualpurge.html?action=9&empty=10,","reportgroupid":"-1","tabtype":"setting","groupjsonflag":"0","displaytitle":"reportlabels.Report_Settings","level3":"-1"},{"appController":"iview","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","description":"{\"content\": \"reportlabels.BookmarkMgMtDesc\"}","label":"reportlabels.Bookmark_Management","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","title":"reportlabels.Bookmark_Management","url":"managebookmark.html?action=79&empty=11,","reportgroupid":"-1","tabtype":"setting","groupjsonflag":"0","displaytitle":"reportlabels.Report_Settings","level3":"-1"},{"appController":"iview","reportgroupid":"-1","module":"REPORTS","validator":"function(module, aclEntity) {return validateMenuItem(module, aclEntity)}","label":"reportlabels.Custom_Logo","aclEntity":"ACLEntityConstant.REPORTS_ACCESS","tabtype":"setting","title":"reportlabels.Custom_Logo","groupjsonflag":"0","displaytitle":"reportlabels.Report_Settings","url":"imageuploadconf.html?action=92&empty=12,","level3":"-1"}];
		Cyberoam.reportMenuArr = menuArr[0].childNodes[2].childNodes;
	}
	var menu = MenuAndTab(document.getElementById('left-menu-container'), menuArr); // Init menu
	// top-left user account drop-down - START
	function fetchHAInfo() {
		const haInfo = JSON.parse('{"hamode":0,"status":"HA not configured"}');
		if (haInfo && haInfo.status === HAConfigurationHelper.HA_CONFIGURED) {
			renderAccountDropDown(true, haInfo);
		} else {
			renderAccountDropDown(false);
		}
	}
	function openSupport(){
		var avoidCSRFInURL=true;
		window.open(OEMProperty.Support_URL,'_blank', '', avoidCSRFInURL);
	}
	function renderAccountDropDown(isHAEnabled, nodes) {
		var accMenuItems=new Array();
		var accMenuTitle = Cyberoam.name;
        var accMenuTitleClass = '';
		
			accMenuTitle = accMenuTitle + '@' + 'boston.toews.io';
		
		if (isHAEnabled) {
            accMenuTitle = nodes.nodename;
            
                accMenuTitle += '-' + 'boston.toews.io';
            
			var clusterTitle = getTitleFromHAstates(nodes);
			if (clusterTitle !== undefined) {
				accMenuItems.push({
					label: clusterTitle,
					noClick: true,
					itemClass: 'simple-text'
				});
			}
			var statusObject = getHAModeAndColour(nodes);
            accMenuTitleClass = statusObject.titleClass;
			accMenuItems.push({
				labels: [
					Cyberoam.getTranslatedMSG("Language." + statusObject.currDevice) + " (" + Cyberoam.getTranslatedMSG("Language.HA_" + statusObject.currState) + ")",
					nodes.nodename,
					nodes.ownappkey
				],
				multilineLabel: true,
				isItemIconDiv: true,
				iconClass: 'icon-status ' + statusObject.currColourClass,
				index: 1
			});
			accMenuItems.push({
				labels: [
					Cyberoam.getTranslatedMSG("Language." + statusObject.peerDevice) + " (" + Cyberoam.getTranslatedMSG("Language.HA_" + statusObject.peerState) + ")",
					nodes.peer_nodename,
					nodes.peerappkey
				],
				multilineLabel: true,
				isItemIconDiv: true,
				iconClass: 'icon-status ' + statusObject.peerColourClass,
				index: 2
			});
			accMenuItems.push({
				isSeparator: true,
				itemClass: 'ha-separator',
				index: 3
			});
		}
		accMenuItems.push({
			label:Language.Support,
			funcName:openSupport,
			index:4
		});
		if(typeof objectArray[ACLEntityConstant.LICENSING] == "undefined") {
			accMenuItems.push({
				label:Language.aboutCyberoam,
				funcName:function(){menu.displayMenuByURL('/registration/ModuleLicense.jsp');},
				index:5
			});
		}
		if(Cyberoam.loginUserName == "admin" || Cyberoam.loginUserName == "support"){
			accMenuItems.push({
				label:Language.CLI,
				funcName:function(){openCLIWindow()},
				index:6
			});
		}
		if(typeof objectArray[ACLEntityConstant.RebootShutdown] == "undefined") {
			accMenuItems.push({
				label:Language.RebootAppliance,
				funcName:function(){ Cyberoam.showPopup({URL:'/ShutdownAppliance.html?reboot=1&amp;operation='+Modes.SHUTDOWN_APPLIANCE,width:450,height:310,title:Language.RebootAppliance});},
				index:7
			});
			accMenuItems.push({
				label:Language.ShutdownAppliance,
				funcName:function(){Cyberoam.showPopup({URL:'/ShutdownAppliance.html?reboot=0&operation='+Modes.SHUTDOWN_APPLIANCE,width:450,height:310,title:Language.ShutdownAppliance});},
				index:8
			});
		}
		if(!Cyberoam.isCentralLogin){
			accMenuItems.push({
				label:Language.Logout,
				funcName:function(){
					javascript:location.href='/webconsole/webpages/logout.jsp';
				},
				index:9
			});
		}
		if(accMenuTitle.length > 40){
			accMenuTitle = accMenuTitle.substring(0,40) + '...';
		}
		var accDropDownConfig = {
			menuClass: "acc-btn",
			menuClassSelect: "selected",
			menuIconClass: "fa fa-caret-down",
			menuDropDownClass: "menu",
			title: accMenuTitle,
            titleClass: accMenuTitleClass,
			menuItems: accMenuItems
		};
		React.render(React.createElement(DropDownMenu, {config: accDropDownConfig}),
				$("#acc-btn")[0]);
	}
	function getTitleFromHAstates(nodes) {
		if (nodes.haconfigmode === HAConfigurationHelper.ACTIVE_PASSIVE_MODE) {
			return Cyberoam.getTranslatedMSG("Language.Active_Passive_Cluster");
		}
		else {
			return Cyberoam.getTranslatedMSG("Language.Active_Active_Cluster");
		}
	}
	function getHAModeAndColour(nodes) {
		var currDevice = peerDevice = HAConfigurationHelper.AUXILIARY_DEV;
		var currColourClass = peerColourClass = "status-green";
		var currState = peerState = "";
		const currMode = HAConfigurationHelper.MODES[nodes.ownstatus];
		const peerMode = HAConfigurationHelper.MODES[nodes.peerstatus];
		if (nodes.hamode === HAConfigurationHelper.ENABLE) {
            var titleClass = "ha-title ";
			switch (currMode) {
				case HAConfigurationHelper.MODES[HAConfigurationHelper.NOT_AVAILABLE]:
					currColourClass = "status-gray";
					break;
				case HAConfigurationHelper.MODES[HAConfigurationHelper.FAULT]:
					currColourClass = "status-red";
					peerDevice = HAConfigurationHelper.PRIMARY_DEV;
					break;
				case HAConfigurationHelper.MODES[HAConfigurationHelper.AUXILIARY]:
                    // keep default values as set
                    break;
				case HAConfigurationHelper.MODES[HAConfigurationHelper.STANDALONE]:
					currDevice = HAConfigurationHelper.PRIMARY_DEV;
					currColourClass = "status-orange";
					break;
				default:
					currDevice = HAConfigurationHelper.PRIMARY_DEV;
			}
			switch (peerMode) {
				case HAConfigurationHelper.MODES[HAConfigurationHelper.NOT_AVAILABLE]:
					peerColourClass = "status-gray";
					break;
				case HAConfigurationHelper.MODES[HAConfigurationHelper.FAULT]:
					peerColourClass = "status-red";
					break;
				case HAConfigurationHelper.MODES[HAConfigurationHelper.PRIMARY]:
					peerDevice = HAConfigurationHelper.PRIMARY_DEV;
					break;
				case HAConfigurationHelper.MODES[HAConfigurationHelper.STANDALONE]:
					peerColourClass = "status-orange";
					break;
			}
			if ((currMode === HAConfigurationHelper.PRIMARY_DEV && peerMode === HAConfigurationHelper.AUXILIARY_DEV) || 
				(currMode === HAConfigurationHelper.AUXILIARY_DEV && peerMode === HAConfigurationHelper.PRIMARY_DEV) ) {
				// both are in good state
                titleClass += "title-green";
				if (nodes.haconfigmode === HAConfigurationHelper.ACTIVE_PASSIVE_MODE) {
					// either of the device is active, and other is passive
					if (currDevice === HAConfigurationHelper.PRIMARY_DEV) {
						currState = "Active";
						peerState = "Passive";
					} else {
						currState = "Passive";
						peerState = "Active";
					}
				} else {
					// both are active
					currState = peerState = "Active";
				}
			} else {
                titleClass += "title-orange";
				currState = currMode.replaceAll(' ', '');
				peerState = peerMode.replaceAll(' ', '');
			}
			return {
				currDevice,
				peerDevice,
				currColourClass,
				peerColourClass,
				currState,
				peerState,
                titleClass
			};
		}
	}
	// top-left user account drop-down - END
	function openClickHereLink(url) {
		menu.displayMenuByURL(url);
	}
	Cyberoam.startit();
				openClickHereLink('/ControlCenter.html?mode=300&operation=1322');
</script>
<script>
	Cyberoam.currentLanguage = "English";
	Cyberoam.currentTheme = "lite1";
	Cyberoam.isEnableDeanonymization = false;
	Cyberoam.reportinterval = "365";
	Cyberoam.strChart2Attrib = "palette1:1";
	Cyberoam.strChart1Attrib = "palette:1";
	Cyberoam.excelExportCustomization ="0";
	Cyberoam.DATALINK_VERSION_CHECK = false;
	Cyberoam.CR_MIGRATION_DATE = "";
	Cyberoam.CR_TO_SOPHOS_MIG_CHECK = false;
	Cyberoam.CR_TO_SOPHOS_MIGRATION_DATE = "";
	Cyberoam.start = "2024-06-03";
	Cyberoam.end = Cyberoam.start;
	Cyberoam.SystemDateInMills = 1717428070528;
	Cyberoam.LogoImagebase64 = "data:image\/"+"png"+";base64,"+"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";
	Cyberoam.LogoImageExt="png";
	Cyberoam.CustomLogoWidth="0";
	Cyberoam.CustomLogoHeight="0";
	Cyberoam.LogoimageType="default";
</script>
<script type="text/javascript" src="/iview/javascript/report.js?version=077b68eec97ffaa545be811dc65cee99"></script>
<script type="text/javascript">
		Cyberoam.refreshMenu(0);
		Cyberoam.OVERLOAD_MEMORY_FLAG = "0";
		if(Cyberoam.OVERLOAD_MEMORY_FLAG==1){
			
			Cyberoam.setStatusBarMessage(Cyberoam.getTranslatedMSG(reportlabels.memory_overload),500);
		}
</script>
	
<script type="text/javascript" src="/javascript/userSnap.js?v=077b68eec97ffaa545be811dc65cee99"></script>
	<script language="javascript" async="true" type="text/javascript" src="https://cdn.whatfix.com/prod/6c3f43c0-f9be-11eb-8a51-2a8342861064/embed/embed.nocache.js"></script>
</body>
</html>
```

## After Logged In

### SFOS Webadmin Request GET example 1

---

#### Request URL (SFOS Webadmin Request get 1)

``` url
https://boston.toews.io:4444/webconsole/Controller?mode=300&operation=1322&_=1717428051380
```

#### Query string (SFOS Webadmin Request get 1)
``` qeury string
mode=300&operation=1322&_=1717428051380
```

#### Request headers (SFOS Webadmin Request get 1)

``` raw headers
GET /webconsole/Controller?mode=300&operation=1322&_=1717428051380 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Cookie: JSESSIONID=yrlybf54kw8zv264lzltyq7v177814; wfx_unq=7tNYD7LafL4ANyOm
DNT: 1
Host: boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/index.jsp
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
X-CSRF-Token: mfd4du0g7dnmvmb5pa8assf1bp
X-Requested-With: XMLHttpRequest
sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

#### Response headers (SFOS Webadmin Request get 1)

``` raw headers
HTTP/1.1 200 OK
Date: Mon, 03 Jun 2024 15:21:11 GMT
Server: xxxx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Content-Type: text/plain;  charset=UTF-8
Cache-Control: max-age=2592000
Expires: Wed, 03 Jul 2024 15:21:11 GMT
Content-Length: 481
Connection: close
```

#### Response body (SFOS Webadmin Request get 1)

``` json
{"isOEM":false,"appliance":{"serial":"X23001RQQV66831","publicKey":"jGzTF7E@9NfUN}y@","url":"https://www.sophos.com/en-us/utility-items/evaluations.aspx?args="},"MandatoryFwUpdateFlag":{},"allowed":1,"now":{"year":2024,"month":6,"day":3,"hour":11,"minute":21,"second":11},"isAuxNode":false,"encryptionInitialized":true,"showEncryptionPopup":false,"ssl":{"tlsInspection":false,"threshold":90,"failedResetTime":"2020-01-01 00:00:00","capacity":18432},"showChangePasswordPopup":false}
```

### SFOS Webadmin Request GET example 2

---

#### Request URL (SFOS Webadmin Request get 2)

``` url
https://boston.toews.io:4444/webconsole/Controller?&mode=1284&json={}&__RequestType=ajax&t=17
```

#### Query string (SFOS Webadmin Request get 2)
``` qeury string
&mode=1284&json={}&__RequestType=ajax&t=1717428051745
```

#### Request headers (SFOS Webadmin Request get 2)

``` raw headers
GET /webconsole/Controller?&mode=1284&json={}&__RequestType=ajax&t=1717428051745 HTTP/1.1
Accept: text/plain, */*; q=0.01
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Cookie: JSESSIONID=yrlybf54kw8zv264lzltyq7v177814; wfx_unq=7tNYD7LafL4ANyOm
DNT: 1
Host: boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/index.jsp
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
X-CSRF-Token: mfd4du0g7dnmvmb5pa8assf1bp
X-Requested-With: XMLHttpRequest
sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

#### Response headers (SFOS Webadmin Request get 2)

``` raw headers
HTTP/1.1 200 OK
Date: Mon, 03 Jun 2024 15:21:11 GMT
Server: xxxx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Content-Type: text/plain;charset=utf-8
Content-Length: 27
Cache-Control: max-age=2592000
Expires: Wed, 03 Jul 2024 15:21:11 GMT
Connection: close
```

#### Response body (SFOS Webadmin Request get 2)

``` json
{"HA_TYPE":"Not Available"}
```

### SFOS Webadmin Request POST example 1

---

#### Request headers (SFOS Webadmin Request post 1)

``` raw headers
POST /webconsole/Controller HTTP/1.1
Accept: text/plain, */*; q=0.01
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Content-Length: 107
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: JSESSIONID=yrlybf54kw8zv264lzltyq7v177814; wfx_unq=7tNYD7LafL4ANyOm
DNT: 1
Host: boston.toews.io:4444
Origin: https://boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/index.jsp
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
X-CSRF-Token: mfd4du0g7dnmvmb5pa8assf1bp
X-Requested-With: XMLHttpRequest
sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

#### Response headers (SFOS Webadmin Request post 1)

``` raw headers
HTTP/1.1 200 OK
Date: Mon, 03 Jun 2024 15:21:12 GMT
Server: xxxx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Content-Type: text/plain;  charset=UTF-8
Content-Length: 437
Cache-Control: max-age=2592000
Expires: Wed, 03 Jul 2024 15:21:12 GMT
Connection: close
```

#### Request body (SFOS Webadmin Request post 1)

``` raw
mode=1322&requestObj={"haInfo":1,"uptime":1,"sfmInfo":1,"centralInfo":1}&__RequestType=ajax&t=1717428053017
```

#### Response body (SFOS Webadmin Request post)

``` json
{"haInfo":{"primaryAppKey":"X23001RQQV66831","currMode":"","dedicatedPort":"-","auxiliaryAppKey":"","monitoredInterfaceList":"","peerMode":"","ownConnection":"","peerConnection":"0","haMode":0,"haConfigMode":0},"centralInfo":{"accountname":"Sophos Ltd","cmstatus":2,"joinmethod":"Manual","managedsince":"November 14, 2022 08:08:52","ztnaStatus":1,"email":"alan@utmtools.com"},"uptime":{"systemuptime":"158 days, 14 hours, 51 minutes\n"}}
```

### SFOS Webadmin Request POST example 2

---

#### Request headers (SFOS Webadmin Request post 2)

``` raw headers
POST /webconsole/Controller HTTP/1.1
Accept: text/plain, */*; q=0.01
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Content-Length: 69
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: JSESSIONID=yrlybf54kw8zv264lzltyq7v177814; wfx_unq=7tNYD7LafL4ANyOm
DNT: 1
Host: boston.toews.io:4444
Origin: https://boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/index.jsp
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
X-CSRF-Token: mfd4du0g7dnmvmb5pa8assf1bp
X-Requested-With: XMLHttpRequest
sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

#### Response headers (SFOS Webadmin Request post 2)

``` raw headers
HTTP/1.1 200 OK
Date: Mon, 03 Jun 2024 15:21:12 GMT
Server: xxxx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Content-Type: text/plain;  charset=UTF-8
Content-Length: 23
Cache-Control: max-age=2592000
Expires: Wed, 03 Jul 2024 15:21:12 GMT
Connection: close
```

#### Request body (SFOS Webadmin Request post 2)

``` raw
mode=1322&requestObj={"cpuInfo":1}&__RequestType=ajax&t=1717428053019
```

#### Response body (SFOS Webadmin Request post 2)

``` json
{"cpuInfo":{"cores":4}}
```

### SFOS Webadmin Request POST example 3

---

#### Request headers (SFOS Webadmin Request post 3)

``` raw headers
POST /webconsole/Controller HTTP/1.1
Accept: text/plain, */*; q=0.01
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Content-Length: 74
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: JSESSIONID=yrlybf54kw8zv264lzltyq7v177814; wfx_unq=7tNYD7LafL4ANyOm
DNT: 1
Host: boston.toews.io:4444
Origin: https://boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/index.jsp
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
X-CSRF-Token: mfd4du0g7dnmvmb5pa8assf1bp
X-Requested-With: XMLHttpRequest
sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

#### Response headers (SFOS Webadmin Request post 3)

``` raw headers
HTTP/1.1 200 OK
Date: Mon, 03 Jun 2024 15:21:12 GMT
Server: xxxx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Content-Type: text/plain;charset=utf-8
Content-Length: 414
Cache-Control: max-age=2592000
Expires: Wed, 03 Jul 2024 15:21:12 GMT
Connection: close
```

#### Request body (SFOS Webadmin Request post 3)

``` raw
mode=1329&json={"reqmode":"svr_status"}&__RequestType=ajax&t=1717428053021
```

#### Response body (SFOS Webadmin Request post 3)

``` json
{"transactionID":"2927423","status":200,"message":"","SFOS Webadmin RequestMessage":"1","entity":{"map":{"mode":1329,"currentlyloggedinuserid":3,"___serverport":4444,"___component":"GUI","APIVersion":"2000.1","___serverprotocol":"HTTP","reqmode":"svr_status","___username":"admin","transactionid":"2927423","___meta":{"map":{"sessionType":1}},"___serverip":"10.5.2.1","currentlyloggedinuserip":"10.5.2.30"}},"redirectionURL":""}
```

### SFOS Webadmin Request POST example 4

---

#### Request headers (SFOS Webadmin Request post 4)

``` raw headers
POST /webconsole/Controller HTTP/1.1
Accept: text/plain, */*; q=0.01
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Content-Length: 73
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: JSESSIONID=yrlybf54kw8zv264lzltyq7v177814; wfx_unq=7tNYD7LafL4ANyOm
DNT: 1
Host: boston.toews.io:4444
Origin: https://boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/index.jsp
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
X-CSRF-Token: mfd4du0g7dnmvmb5pa8assf1bp
X-Requested-With: XMLHttpRequest
sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

#### Response headers (SFOS Webadmin Request post 4)

``` raw headers
HTTP/1.1 200 OK
Date: Mon, 03 Jun 2024 15:21:12 GMT
Server: xxxx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Content-Type: text/plain;  charset=UTF-8
Content-Length: 348
Cache-Control: max-age=2592000
Expires: Wed, 03 Jul 2024 15:21:12 GMT
Connection: close
```

#### Request body (SFOS Webadmin Request post 4)

``` raw
mode=1322&requestObj={"networkInfo":1}&__RequestType=ajax&t=1717428053022
```

#### Response body (SFOS Webadmin Request post 4)

``` json
{"networkInfo":{"gatewaydata":{"downGatewayList":[{"ipaddress":"128.69.69.128","gatewayname":"Nowhere","interface":"br0"}],"count":"4","gwstatus":"1","status":2},"interfacedata":{"interfacesList":[{"ipaddress":"169.254.192.1","netmask":"255.255.255.0","zonetype":"3","interface":"PortMGMT"}],"status":2},"dhcpdata":{"dhspwithoutip":[],"status":0}}}
```

### SFOS Webadmin Request POST example 5

---

#### Request headers (SFOS Webadmin Request post 5)

``` raw headers
POST /webconsole/Controller HTTP/1.1
Accept: text/plain, */*; q=0.01
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Content-Length: 69
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: JSESSIONID=yrlybf54kw8zv264lzltyq7v177814; wfx_unq=7tNYD7LafL4ANyOm
DNT: 1
Host: boston.toews.io:4444
Origin: https://boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/index.jsp
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
X-CSRF-Token: mfd4du0g7dnmvmb5pa8assf1bp
X-Requested-With: XMLHttpRequest
sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

#### Response headers (SFOS Webadmin Request post 5)

``` raw headers
HTTP/1.1 200 OK
Date: Mon, 03 Jun 2024 15:21:12 GMT
Server: xxxx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Content-Type: text/plain;  charset=UTF-8
Content-Length: 352
Cache-Control: max-age=2592000
Expires: Wed, 03 Jul 2024 15:21:12 GMT
Connection: close
```

#### Request body (SFOS Webadmin Request post 5)

``` raw
mode=1322&requestObj={"vpnInfo":1}&__RequestType=ajax&t=1717428053023
```

#### Response body (SFOS Webadmin Request post 5)

``` json
{"vpnInfo":{"VPNData":[{"conncount":"0","keymode":"a","conntype":"xfrmi","connectionname":"Central_10_5_33_85_tokyo_toews_io_QFM7BjWpr7","connectionid":"5","groupname":"-","status":"2"},{"conncount":"0","keymode":"a","conntype":"xfrmi","connectionname":"Central_10_5_33_81_london_toews_io_nSUE6IAGhC","connectionid":"3","groupname":"-","status":"2"}]}}
```

### SFOS Webadmin Request POST example 6

---

#### Request headers (SFOS Webadmin Request post 6)

``` raw headers
POST /webconsole/Controller HTTP/1.1
Accept: text/plain, */*; q=0.01
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Content-Length: 70
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: JSESSIONID=yrlybf54kw8zv264lzltyq7v177814; wfx_unq=7tNYD7LafL4ANyOm
DNT: 1
Host: boston.toews.io:4444
Origin: https://boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/index.jsp
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
X-CSRF-Token: mfd4du0g7dnmvmb5pa8assf1bp
X-Requested-With: XMLHttpRequest
sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

#### Response headers (SFOS Webadmin Request post 6)

``` raw headers
HTTP/1.1 200 OK
Date: Mon, 03 Jun 2024 15:21:12 GMT
Server: xxxx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Content-Type: text/plain;  charset=UTF-8
Content-Length: 105
Cache-Control: max-age=2592000
Expires: Wed, 03 Jul 2024 15:21:12 GMT
Connection: close
```

#### Request body (SFOS Webadmin Request post 6)

``` raw
mode=1322&requestObj={"hbStatus":1}&__RequestType=ajax&t=1717428053024
```

#### Response body (SFOS Webadmin Request post 6)

``` json
{"hbStatus":{"registered":true,"hbEnabled":true,"status":{"red":"0","green":0,"yellow":"0","missing":0}}}
```

### SFOS Webadmin Request POST example 7

---

#### Request headers (SFOS Webadmin Request post 7)

``` raw headers
POST /webconsole/Controller HTTP/1.1
Accept: text/plain, */*; q=0.01
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Content-Length: 152
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: JSESSIONID=yrlybf54kw8zv264lzltyq7v177814; wfx_unq=7tNYD7LafL4ANyOm
DNT: 1
Host: boston.toews.io:4444
Origin: https://boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/index.jsp
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
X-CSRF-Token: mfd4du0g7dnmvmb5pa8assf1bp
X-Requested-With: XMLHttpRequest
sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

#### Response headers (SFOS Webadmin Request post 7)

``` raw headers
HTTP/1.1 200 OK
Date: Mon, 03 Jun 2024 15:21:13 GMT
Server: xxxx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Content-Type: text/plain;  charset=UTF-8
Content-Length: 262
Cache-Control: max-age=2592000
Expires: Wed, 03 Jul 2024 15:21:13 GMT
Connection: close
```

#### Request body (SFOS Webadmin Request post 7)

``` raw
mode=1322&requestObj={"eacAllAppsCount":1,"eacNewAppsCount":1,"eacCategorizedAppsCount":1,"hbStatus":1,"eacStatus":1}&__RequestType=ajax&t=1717428053034
```

#### Response body (SFOS Webadmin Request post 7)

``` json
{"hbStatus":{"registered":true,"hbEnabled":true,"status":{"red":"0","green":0,"yellow":"0","missing":0}},"eacAllAppsCount":{"eacAllAppsCount":2344},"eacStatus":true,"eacNewAppsCount":{"eacNewAppsCount":68},"eacCategorizedAppsCount":{"eacCategorizedAppsCount":4}}
```

### SFOS Webadmin Request POST example 8

---

#### Request headers (SFOS Webadmin Request post 8)

``` raw headers
POST /webconsole/Controller HTTP/1.1
Accept: text/plain, */*; q=0.01
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Content-Length: 71
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: JSESSIONID=yrlybf54kw8zv264lzltyq7v177814; wfx_unq=7tNYD7LafL4ANyOm
DNT: 1
Host: boston.toews.io:4444
Origin: https://boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/index.jsp
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
X-CSRF-Token: mfd4du0g7dnmvmb5pa8assf1bp
X-Requested-With: XMLHttpRequest
sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

#### Response headers (SFOS Webadmin Request post 8)

``` raw headers
HTTP/1.1 200 OK
Date: Mon, 03 Jun 2024 15:21:13 GMT
Server: xxxx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Content-Type: text/plain;  charset=UTF-8
Content-Length: 87
Cache-Control: max-age=2592000
Expires: Wed, 03 Jul 2024 15:21:13 GMT
Connection: close
```

#### Request body (SFOS Webadmin Request post 8)

``` raw
mode=1322&requestObj={"atpStatus":1}&__RequestType=ajax&t=1717428053037
```

#### Response body (SFOS Webadmin Request post 8)

``` json
{"atpStatus":{"sourceCount":1,"mdrEnabled":true,"count":1,"mdrCount":0,"enabled":true}}
```

### SFOS Webadmin Request POST example 9

---

#### Request headers (SFOS Webadmin Request post 9)

``` raw headers
POST /webconsole/Controller HTTP/1.1
Accept: text/plain, */*; q=0.01
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Content-Length: 71
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: JSESSIONID=yrlybf54kw8zv264lzltyq7v177814; wfx_unq=7tNYD7LafL4ANyOm
DNT: 1
Host: boston.toews.io:4444
Origin: https://boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/index.jsp
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
X-CSRF-Token: mfd4du0g7dnmvmb5pa8assf1bp
X-Requested-With: XMLHttpRequest
sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

#### Response headers (SFOS Webadmin Request post 9)

``` raw headers
HTTP/1.1 200 OK
Date: Mon, 03 Jun 2024 15:21:13 GMT
Server: xxxx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Content-Type: text/plain;  charset=UTF-8
Content-Length: 87
Cache-Control: max-age=2592000
Expires: Wed, 03 Jul 2024 15:21:13 GMT
Connection: close
```

#### Request body (SFOS Webadmin Request post 9)

``` raw
mode=1322&requestObj={"atpStatus":1}&__RequestType=ajax&t=1717428053039
```

#### Response body (SFOS Webadmin Request post 9)

``` json
{"atpStatus":{"sourceCount":1,"mdrEnabled":true,"count":1,"mdrCount":0,"enabled":true}}
```

### SFOS Webadmin Request POST example 10

---

#### Request headers (SFOS Webadmin Request post 10)

``` raw headers
Accept: text/plain, */*; q=0.01
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Content-Length: 79
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: JSESSIONID=yrlybf54kw8zv264lzltyq7v177814; wfx_unq=7tNYD7LafL4ANyOm
Dnt: 1
Host: boston.toews.io:4444
Origin: https://boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/index.jsp
Sec-Ch-Ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
X-Csrf-Token: mfd4du0g7dnmvmb5pa8assf1bp
X-Requested-With: XMLHttpRequest
```

#### Response headers (SFOS Webadmin Request post 10)

``` raw headers
HTTP/1.1 200 OK
Date: Mon, 03 Jun 2024 15:21:13 GMT
Server: xxxx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Content-Type: text/plain;  charset=UTF-8
Content-Length: 36
Cache-Control: max-age=2592000
Expires: Wed, 03 Jul 2024 15:21:13 GMT
Connection: close
```

#### Request body (SFOS Webadmin Request post 10)

``` raw
mode=1328&json={}&requestObj={"redStatus":1}&__RequestType=ajax&t=1717428053043
```

#### Response body (SFOS Webadmin Request post 10)

``` json
{"redStatus":{"total":0,"active":0}}
```

### SFOS Webadmin Request POST example 11

---

#### Request headers (SFOS Webadmin Request post 11)

``` raw headers
POST /webconsole/Controller HTTP/1.1
Accept: text/plain, */*; q=0.01
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Content-Length: 73
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: JSESSIONID=yrlybf54kw8zv264lzltyq7v177814; wfx_unq=7tNYD7LafL4ANyOm
DNT: 1
Host: boston.toews.io:4444
Origin: https://boston.toews.io:4444
Referer: https://boston.toews.io:4444/webconsole/webpages/index.jsp
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0
X-CSRF-Token: mfd4du0g7dnmvmb5pa8assf1bp
X-Requested-With: XMLHttpRequest
sec-ch-ua: "Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

#### Response headers (SFOS Webadmin Request post 11)

``` raw headers
HTTP/1.1 200 OK
Date: Mon, 03 Jun 2024 15:21:13 GMT
Server: xxxx
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
Content-Type: text/plain;  charset=UTF-8
Content-Length: 27
Cache-Control: max-age=2592000
Expires: Wed, 03 Jul 2024 15:21:13 GMT
Connection: close
```

#### Request body (SFOS Webadmin Request post 11)

``` raw
mode=1322&requestObj={"remoteUsers":1}&__RequestType=ajax&t=1717428053045
```

#### Response body (SFOS Webadmin Request post 11)

``` json
{"remoteUsers":{"count":0}}
```

