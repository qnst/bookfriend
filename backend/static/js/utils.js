/**
 * Created by wangsanyang on 2015/8/13.
 */

// 拼接某个元素内带有name属性的元素的值
function getParams(elem){
    var params={};
    $(elem).find("*").each(function(){
        if($(this).attr("name")){
            var key=$(this).attr("name");
            var value="";
            if($(this).val()){
                value=$(this).val();
            }else{
                value=$(this).text()
            }
            if(value!=""){
                params[key]=value;
            }
        }
    });
    return params;
}

// 操作URL参数
var LG = (function (lg) {
    var objURL = function (url) {
        this.ourl = url || window.location.href;
        this.href = "";//?前面部分
        this.params = {};//url参数对象
        this.jing = "";//#及后面部分
        this.init();
    }
    //分析url,得到?前面存入this.href,参数解析为this.params对象，#号及后面存入this.jing
    objURL.prototype.init = function () {
        var str = this.ourl;
        var index = str.indexOf("#");
        if (index > 0) {
            this.jing = str.substr(index);
            str = str.substring(0, index);
        }
        index = str.indexOf("?");
        if (index > 0) {
            this.href = str.substring(0, index);
            str = str.substr(index + 1);
            var parts = str.split("&");
            for (var i = 0; i < parts.length; i++) {
                var kv = parts[i].split("=");
                this.params[kv[0]] = kv[1];
            }
        }
        else {
            this.href = this.ourl;
            this.params = {};
        }
    }
    //只是修改this.params
    objURL.prototype.set = function (key, val) {
        this.params[key] = val;
    }
    //只是设置this.params
    objURL.prototype.remove = function (key) {
        this.params[key] = undefined;
    }
    //根据三部分组成操作后的url
    objURL.prototype.url = function () {
        var strurl = this.href;
        var objps = [];//这里用数组组织,再做join操作
        for (var k in this.params) {
            if (this.params[k]) {
                objps.push(k + "=" + this.params[k]);
            }
        }
        if (objps.length > 0) {
            strurl += "?" + objps.join("&");
        }
        if (this.jing.length > 0) {
            strurl += this.jing;
        }
        return strurl;
    }
    //得到参数值
    objURL.prototype.get = function (key) {
        return this.params[key];
    }
    lg.URL = objURL;
    return lg;
}(LG || {}));

// 全不选
function uncheckall() {
    $("table :checkbox:gt(0)").each(function () {
                $(this).attr("checked", false)
            }
    )
}

// 全选
function checkall() {
    uncheckall()
    $("table :checkbox:gt(0)").each(function () {
        $(this).click()
    })
}

// 获取选中项（checkbox的value设为主键id，额外属性以extra1/extra2这种格式定义）
function get_checked(){
    var checkedValue = '';
    var res = {"flag": 0, "ids": '', "extras":[]}  //flag:选中的个数；ids:主键id以,分割；extras:额外参数集合
    $('[name="id_checkalln"]:checked').each(function(){
        $input = $(this)
        res['flag'] += 1 ;
        checkedValue += $input.val() + ',';
        $.each([1,2,3],function(){  // 定义了三个额外属性，可以根据实际情况来增加
            extra_name = 'extra'+this  // extra1/extra2/extra3
            extra_value = $input.attr(extra_name)
            if (extra_value){
                var extra_json = {}
                extra_json[extra_name] = extra_value
                res['extras'].push(extra_json)
            }
        })
    });
    if (checkedValue.length > 0){
        res['ids'] = checkedValue.substr(0, checkedValue.length-1)
    }
    return res
}

// 字符串拼接，例 '{0}---{1}'.format('a', 'b')
String.prototype.format = function() {
    var result=this;
    if (arguments.length == 0)
        return null;
    for ( var i = 0; i < arguments.length; i++) {
        var re = new RegExp('\\{' + (i) + '\\}', 'gm');
        result = result.replace(re, arguments[i]);
    }
    return result;
};

// 同步post提交: 成功(code==0)，刷新页面;失败(code!=0),则弹出错误信息
function sync_post(url, params){
     $.ajax({
         type: 'post',
         url: url,
         data: params,
         async: false,
         dataType: 'json',
         success: function(data){
             if (data.code == 0){  // 只适用于提交后不跳转的抢矿
                     window.location.reload();
                }
             else{
                var d = dialog({
                    title: '错误！',
                    content: data.message.toString()
                });
                 d.showModal();
             }
         }
     })
}

// 添加气泡提示消息
function add_tip(criteria, tip){
    $(criteria).on("mouseover", function(){
        var d = dialog({
            content: tip,
            quickClose: true// 点击空白处快速关闭
        });
        d.show($(this)[0]);
    });
}

// 字符串是否在数组中
function in_array(stringToSearch, arrayToSearch) {
    for (s = 0; s < arrayToSearch.length; s++) {
        thisEntry = arrayToSearch[s].toString();
        if (thisEntry == stringToSearch) {
            return true;
        }
    }
    return false;
}

// 格式化时间
var formatDateTime = function (date) {
    var y = date.getFullYear();
    var m = date.getMonth() + 1;
    m = m < 10 ? ('0' + m) : m;
    var d = date.getDate();
    d = d < 10 ? ('0' + d) : d;
    var h = date.getHours();
    var minute = date.getMinutes();
    minute = minute < 10 ? ('0' + minute) : minute;
    return y + '-' + m + '-' + d+' '+h+':'+minute;
};

// 获取一个时间段
function get_start_end_time(_type){
    var now = new Date();
    var endtime = formatDateTime(now);
    var starttime;
    switch (_type){
        case "real_time":  // 十分钟
            starttime = now.setMinutes(now.getMinutes()-10);
            break;
        case "last_three_hours":
            starttime = now.setHours(now.getHours()-3);
            break;
        case "last_one_day":
            starttime = now.setHours(now.getHours()-24);
            break;
        case "last_one_week":
            starttime = now.setDate(now.getDate()-7);
            break;
        case "last_one_month":
            starttime = now.setMonth(now.getMonth()-1);
            break;
        case "last_three_month":
            starttime = now.setMonth(now.getMonth()-3);
            break;
        default:
            alert('没有定义的方式： ' + _type);
    }
    starttime = new Date(starttime);  // 把时间戳转换为时间格式
    starttime = formatDateTime(starttime);  // 把时间格式转换为字符串
    return [starttime, endtime];
}