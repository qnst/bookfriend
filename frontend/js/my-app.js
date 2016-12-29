// Initialize your app
var myApp = new Framework7({
    modalTitle: '书友',  // Default title for modals (Alert, Confirm, Prompt)
    modalButtonOk: '确认',
    modalButtonCancel: '取消',

    template7Pages: true,
    pushState: true,  // If it is webapp, we can enable hash navigation:

    onAjaxStart: function (xhr) {
        myApp.showIndicator();
    },
    onAjaxComplete: function (xhr) {
        myApp.hideIndicator();
    },

    // // 未登录用户跳转到登陆页面
    // preroute: function (view, options) {
    //     if (!userLoggedIn) {
    //         view.router.loadPage('auth.html'); //load another page with auth form
    //         return false; //required to prevent default router action
    //     }
    // },

    // 页面预加载
    preprocess: function (content, url, next) {
        console.log(url);
        if (url === 'people.html') {
            var template = Template7.compile(content);
            var resultContent = template({
                title: 'People',
                people: ['John', 'Ivan', 'Mary']
            });
            return resultContent;
        }else{
            return content;
        }
    }
});

// Export selectors engine
var $$ = Dom7;

// Add views
var view1 = myApp.addView('#view-1');
var view2 = myApp.addView('#view-2', {
    dynamicNavbar: true
});
var view3 = myApp.addView('#view-3');
var view4 = myApp.addView('#view-4');



// 页面初始化方式一
myApp.onPageInit('about', function (page) {
    console.log(page);
    // myApp.alert('Here is an about page.');
});

// myApp.onPageInit('search', function (page) {
//     console.log('xxxx');
//     var mySearchbar = app.searchbar('.searchbar', {
//         // searchList: '.list-block-search',
//         // searchIn: '.item-title',
//         customSearch: true,
//         onSearch: function (s) {
//             console.log(s);
//             console.log(s.query);
//         }
//     });
//     mySearchbar.search('追风筝的人');
// });
// myApp.init();

// // 页面初始化方法二
// $$(document).on('pageInit', function (e) {
//     var page = e.detail.page;
//     // Code for About page
//     if (page.name === 'about') {
//         var count = page.query.count;
//     }
// }