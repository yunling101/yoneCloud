var gulp = require("gulp");
var cssmin = require('gulp-cssmin');
var htmlmin = require('gulp-htmlmin');
var $ = require("gulp-load-plugins")();
var clean = require('gulp-clean');

gulp.task('clean', function () {
   return gulp.src('./public/dist/', {
      allowEmpty: true
   })
      .pipe(clean())
})

gulp.task('img', function () {
   return gulp.src([
      "./public/src/img/*",
   ])
      .pipe(gulp.dest('./public/dist/img/'))
})

gulp.task('fonts', function () {
   return gulp.src([
      "./public/src/libs/bootstrap/dist/fonts/*",
      "./public/src/libs/font-awesome/fonts/*",
      "./public/src/fonts/*/**"
   ])
      .pipe(gulp.dest('./public/dist/fonts/'))
})

gulp.task('app', function () {
   return gulp.src("./public/src/css/app.css")
      .pipe($.rename({ suffix: ".min" }))
      .pipe($.cleanCss()) // 兼容性 {compatibility:"ie8"}
      .pipe(cssmin())
      .pipe(gulp.dest("./public/dist/css/"))
})

gulp.task('player_css', function () {
   return gulp.src("./public/src/js/player/player.css")
      .pipe($.rename({ suffix: ".min" }))
      .pipe($.cleanCss())
      .pipe(cssmin())
      .pipe(gulp.dest("./public/dist/css/"))
})

gulp.task('xterm_css', function () {
   return gulp.src("./public/src/js/xterm/addons/fullscreen/fullscreen.css")
      .pipe($.cleanCss())
      .pipe(cssmin())
      .pipe(gulp.dest("./public/dist/css/"))
})

gulp.task('main', function () {
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
      .pipe($.concat("main.min.js"))
      .pipe($.uglify())  // 压缩
      .pipe(gulp.dest("./public/dist/js/"))
})

gulp.task('index', function () {
   return gulp.src("./public/src/js/*.js")
      .pipe($.order([
         "template.js",
         "form.js",
         "table.js",
         "config.js",
         "fast.js",
         "index.js"
      ]))
      .pipe($.concat("index.min.js"))
      .pipe($.uglify())
      .pipe(gulp.dest("./public/dist/js/"))
})

gulp.task('model', function () {
   return gulp.src("./public/src/js/model/**/*.js")
      .pipe($.uglify())
      .pipe(gulp.dest("./public/dist/js/model/"))
})

gulp.task('login', function () {
   return gulp.src("./public/src/js/login/*.js")
      .pipe($.order([
         "jquery.min.js",
         "login.js"
      ]))
      .pipe($.concat("login.min.js"))
      .pipe($.uglify())
      .pipe(gulp.dest("./public/dist/js/"))
})

gulp.task('forgot', function () {
   return gulp.src("./public/src/js/forgot/*.js")
      .pipe($.order([
         "jquery.min.js",
         "forgot.js"
      ]))
      .pipe($.concat("forgot.min.js"))
      .pipe($.uglify())
      .pipe(gulp.dest("./public/dist/js/"))
})

gulp.task('xterm_js', function () {
   return gulp.src("./public/src/js/xterm/**/*.js")
      .pipe($.order([
         "jquery.min.js",
         "xterm.js",
         "addons/fit/fit.js",
         "addons/attach/attach.js",
         "addons/fullscreen/fullscreen.js",
         "sshconnect.js"
      ]))
      .pipe($.concat("connect.min.js"))
      .pipe($.uglify())
      .pipe(gulp.dest("./public/dist/js/xterm/"))
})

gulp.task('player_js', function () {
   return gulp.src("./public/src/js/player/player.js")
      .pipe($.uglify())
      .pipe($.rename({ suffix: ".min" }))
      .pipe(gulp.dest("./public/dist/js/"))
})

gulp.task('copy_locale_select', function () {
   return gulp.src("./public/src/js/lib/locale/bootstrap-select-en_US.js")
      .pipe(gulp.dest("./public/dist/js/locale/"))
})

gulp.task('copy_locale_table', function () {
   return gulp.src("./public/src/js/lib/locale/bootstrap-table-en-US.js")
      .pipe(gulp.dest("./public/dist/js/locale/"))
})

gulp.task('copy_locale', function () {
   return gulp.src("./public/src/js/lib/locale/en-US.js")
      .pipe(gulp.dest("./public/dist/js/locale/"))
})

gulp.task('html', function () {
   return gulp.src("./public/src/*.html")
      .pipe(htmlmin({ removeEmptyAttributes: true, collapseWhitespace: true }))
      .pipe(gulp.dest("./public/dist/html/"))
})

gulp.task('copy_css_images', function () {
   return gulp.src("./public/src/css/images/*")
      .pipe(gulp.dest("./public/dist/css/images/"))
})
gulp.task('copy_lib_duallistbox', function () {
   return gulp.src("./public/src/js/duallistbox/*")
      .pipe(gulp.dest("./public/dist/js/duallistbox/"))
})
gulp.task('copy_lib_theme', function () {
   return gulp.src("./public/src/js/theme/*/**")
      .pipe(gulp.dest("./public/dist/js/theme/"))
})

exports.default = gulp.series('clean',
   gulp.parallel(
      'img',
      'fonts',
      'app',
      'player_css',
      'main',
      'index',
      'model',
      'login',
      'forgot',
      'xterm_css',
      'xterm_js',
      'player_js',
      'html',
      'copy_css_images',
      'copy_lib_duallistbox',
      'copy_lib_theme',
      'copy_locale_select',
      'copy_locale',
   ))