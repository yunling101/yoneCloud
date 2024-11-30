var gulp = require("gulp");
var $ = require("gulp-load-plugins")();
var del = require('del');

function clean() {
   return del(["./public/static/"]);
}

function copy_fonts() {
   return gulp.src([
      "./public/src/libs/bootstrap/dist/fonts/*",
      "./public/src/libs/font-awesome/fonts/*",
      "./public/src/fonts/*/**"
   ])
      .pipe(gulp.dest('./public/static/fonts/'))
      .pipe($.livereload())
}

function copy_img() {
   return gulp.src([
      "./public/src/img/*/**",
   ])
      .pipe(gulp.dest('./public/static/img/'))
      .pipe($.livereload())
}

function build_css() {
   return gulp.src("./public/src/css/app.css")
      .pipe($.concat("app.css"))
      .pipe($.rename({ suffix: ".min" }))
      .pipe($.cleanCss()) // 兼容性 {compatibility:"ie8"}
      .pipe(gulp.dest("./public/static/css/"))
      .pipe($.livereload())
}

function build_player_css() {
   return gulp.src("./public/src/js/player/player.css")
      .pipe($.rename({ suffix: ".min" }))
      .pipe($.cleanCss())
      .pipe(gulp.dest("./public/static/css/"))
}

function build_js_lib() {
   return gulp.src("./public/src/js/lib/*.js") // 找目标文件并读取到gulp内存中
      .pipe($.order([
         "jquery.min.js",
         "popper.min.js",
         "bootstrap.js",
         "jquery.metisMenu.js",
         "jquery.slimscroll.min.js",
         "inspinia.js",
         "jquery-ui.min.js",
         "jquery.validator.min.js",
         "zh-CN.js",
         "bootstrap-table.min.js",
         "bootstrap-table-zh-CN.js",
         "bootstrap-table-commonsearch.js",
         "bootstrap-select.js",
         "bootstrap-select-zh_CN.js",
         "moment.js",
         "daterangepicker.js",
         "Chart.min.js",
         "ejs.min.js"
      ]))
      .pipe($.concat("main.js")) // 临时合并文件
      .pipe(gulp.dest("./public/static/js/")) // 临时输出
      .pipe($.uglify())  // 压缩
      .pipe($.rename({ suffix: ".min" })) // rename("main.min.js") // 重命名
      .pipe(gulp.dest("./public/static/js/"))
}

function build_js() {
   return gulp.src("./public/src/js/*.js")
      .pipe($.order([
         "template.js",
         "form.js",
         "table.js",
         "config.js",
         "fast.js",
         "index.js"
      ]))
      .pipe($.concat("index.js"))
      .pipe(gulp.dest("./public/static/js/"))
      .pipe($.uglify())  // 压缩
      .pipe($.rename({ suffix: ".min" }))
      .pipe(gulp.dest("./public/static/js/"))
      .pipe($.livereload())
}

function build_model() {
   return gulp.src("./public/src/js/model/**/*.js")
      .pipe($.uglify())  // 压缩
      .pipe(gulp.dest("./public/static/js/model/"))
      .pipe($.livereload())
}

function build_login() {
   return gulp.src("./public/src/js/login/*.js")
      .pipe($.order([
         "jquery.min.js",
         "login.js"
      ]))
      .pipe($.concat("login.js"))
      .pipe(gulp.dest("./public/static/js/"))
      .pipe($.uglify())  // 压缩
      .pipe($.rename({ suffix: ".min" }))
      .pipe(gulp.dest("./public/static/js/"))
      .pipe($.livereload())
}

function build_forgot() {
   return gulp.src("./public/src/js/forgot/*.js")
      .pipe($.order([
         "jquery.min.js",
         "forgot.js"
      ]))
      .pipe($.concat("forgot.js"))
      .pipe(gulp.dest("./public/static/js/"))
      .pipe($.uglify())  // 压缩
      .pipe($.rename({ suffix: ".min" }))
      .pipe(gulp.dest("./public/static/js/"))
      .pipe($.livereload())
}

function build_xterm() {
   return gulp.src("./public/src/js/xterm/**/*.js")
      .pipe($.order([
         "jquery.min.js",
         "xterm.js",
         "addons/fit/fit.js",
         "addons/attach/attach.js",
         // "addons/terminado/terminado.js",
         // "addons/search/search.js",
         "addons/fullscreen/fullscreen.js",
         "sshconnect.js"
      ]))
      .pipe($.concat("connect.js"))
      .pipe(gulp.dest("./public/static/js/xterm/"))
      .pipe($.uglify())  // 压缩
      .pipe($.rename({ suffix: ".min" }))
      .pipe(gulp.dest("./public/static/js/xterm/"))
      .pipe($.livereload())
}

function build_player() {
   return gulp.src("./public/src/js/player/player.js")
      .pipe($.uglify())  // 压缩
      .pipe($.rename({ suffix: ".min" }))
      .pipe(gulp.dest("./public/static/js/"))
}

function build_container() {
   return gulp.src("./public/src/js/containerd/*.js")
      .pipe($.order([
         "form.js",
         "table.js",
         "config.js",
         "fast.js",
         "index.js"
      ]))
      .pipe($.concat("index.js"))
      .pipe(gulp.dest("./public/static/js/containerd/"))
      .pipe($.uglify())  // 压缩
      .pipe($.rename({ suffix: ".min" }))
      .pipe(gulp.dest("./public/static/js/containerd/"))
      .pipe($.livereload());
}

function copy_html_model() {
   return gulp.src("./public/src/model/*.html")
      .pipe($.htmlmin({ removeEmptyAttributes: true, collapseWhitespace: true }))
      .pipe(gulp.dest("./public/static/model/"))
      .pipe($.livereload());
}

function build_html() {
   return gulp.src("./public/src/*.html")
      .pipe($.htmlmin({ removeEmptyAttributes: true, collapseWhitespace: true }))
      .pipe(gulp.dest("./public/static/html/"))
      .pipe($.livereload());
}

function compile_html_to_js() {
   return gulp.src("./public/src/html/**/*.html")
      .pipe($.htmlmin({ removeEmptyAttributes: true, collapseWhitespace: true }))
      .pipe($.htmlCompile({
         name: function (file) {
            return file.relative.split('.')[0];
         },
         namespace: 'Templates'
      }
      ))
      .pipe($.concat("template.js"))
      .pipe(gulp.dest("./public/src/js/"))
      .pipe($.livereload());
}

function watch() {
   gulp.watch("./public/src/css/app.css", build_css);
   gulp.watch("./public/src/*.html", build_html);
   gulp.watch("./public/src/html/**/*.html", compile_html_to_js);
   gulp.watch("./public/src/js/*.js", build_js);
   gulp.watch("./public/src/js/model/**/*.js", build_model);
   gulp.watch("./public/src/js/forgot/*.js", build_forgot);
   gulp.watch("./public/src/js/xterm/**/*.js", build_xterm);
   gulp.watch("./public/src/js/containerd/*.js", build_container);
}

var css = gulp.series(gulp.parallel(
   copy_fonts,
   copy_img,
   build_css,
   build_player_css
));

var js = gulp.series(gulp.parallel(
   build_js_lib,
   build_js,
   build_model,
   build_login,
   build_forgot,
   build_xterm,
   build_player,
   build_model
));

var html = gulp.series(
   copy_html_model,
   gulp.parallel(
      build_html,
      compile_html_to_js
   ));

exports.css = css;
exports.js = js;
exports.html = html;
exports.watch = watch;