<template>
  <div>
    <el-dialog
        title="导出数据"
        :visible.sync="dialogVisible"
        width="30%">
      <el-form ref="form">
        <el-form-item label="文件名" prop="perf_filename">
          <el-input v-model="file_name" placeholder="请输入文件名"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="exportData">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog
        title="历史记录"
        :visible.sync="dialogVisible1"
        width="80%">
      <history v-if="dialogVisible1"></history>
    </el-dialog>
    <el-form :inline="true">
      <el-form-item label="设备" class="filter">
        <el-select v-model="selected_device" clearable filterable>
          <el-option v-for="item in device_list" :key="item"
                     :label="item" :value="item"></el-option>
        </el-select>
        <el-button class="btn btn-default" @click="getDeviceList" :disable="getting">
          <i class="el-icon-refresh" v-if="!getting"></i>
          <i class="el-icon-loading" v-if="getting"></i>
        </el-button>
      </el-form-item>
      <el-form-item label="App" class="filter">
        <el-select v-model="selected_app" placeholder="" clearable filterable
                   :multiple="platform==='windows'">
          <el-option v-for="item in package_list" :key="item"
                     :label="item" :value="item"></el-option>
        </el-select>
        <el-button id="restart_app" class="btn btn-default" @click="startAPP(true)">重启
        </el-button>
      </el-form-item>
      <el-form-item label="" class="filter">
        <el-button :disabled="!echart_show" type="primary"
                   @click="startCapture" v-text="startButton">
        </el-button>
        <el-button id="clear_data" type="danger" @click="clearData">清除数据
        </el-button>
        <el-button id="export_data" :disabled="!perf_filepath" type="success"
                   @click="dialogVisible = true">导出数据
        </el-button>
        <el-button id="dump_hprof" class="btn btn-default" @click="dumpHprof"
                   v-if="platform === 'android'">获取hprof
        </el-button>
        <el-button @click="advanced_settting = true" style="margin-left: 10px">更多...</el-button>
      </el-form-item>
      <el-form-item label="布局" class="filter">
        <el-select v-model="layout" @change="changeLayout" style="width: 100px">
          <el-option label="1列1组" :value="1"></el-option>
          <el-option label="1列2组" :value="2"></el-option>
          <el-option label="1列3组" :value="3"></el-option>
          <el-option label="1列4组" :value="4"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="已采集(分钟)" class="filter" v-if="is_capture">
        <el-tag>{{ test_time }}</el-tag>
      </el-form-item>


    </el-form>
    <el-table :data="[perf_chart_data]" style="width: 100%;margin-bottom: 10px">
      <el-table-column v-for="(item, index) in perf_chart_data" v-if="item.show && item.selected"
                       :formatter="setAvgResult"
                       :key="'col'+index"
                       :label="item.title">
      </el-table-column>
    </el-table>
    <div style="margin-bottom: 10px; display: inline-flex; flex-wrap: wrap; justify-content: center">
      <template v-for="(item, index) in perf_chart_data">
        <el-card lazy v-loading="reloading"
                 :key="'card_'+index"
                 v-if="item.show && item.selected"
                 :style="layoutCss">
          <!--            <highcharts :options="echart_obƒject[index]" :constructor-type="'stockChart'"-->
          <!--                        :ref='"chart_"+index'-->
          <!--                        :style="layoutCss2"-->
          <!--            ></highcharts>-->
          <data-chart :data-key="index" :ref='"chart_"+index' :style="layoutCss2" :title="item.title"
                      :data-group="dataGroup"
                      :refresh-time="refreshTime" :capture="is_capture"
                      :label="item.label">

          </data-chart>
        </el-card>
      </template>

    </div>
    <el-drawer
        title="更多设置"
        :visible.sync="advanced_settting"
        :direction="direction"
    >
      <el-card class="box-card" style="margin: 8px">
        <div slot="header" class="clearfix">
          <span>显示图表</span>
        </div>
        <el-checkbox-group v-model="selectData" @change="handleShowChange">
          <el-checkbox v-for="(item,index) in perf_chart_data" :key="index"
                       style="width: 35%;margin: 5px"
                       v-show="item.show"
                       :label="index">{{ item.title }}
          </el-checkbox>
        </el-checkbox-group>
      </el-card>
      <el-card class="box-card" style="margin: 8px">
        <div slot="header" class="clearfix">
          <span>包安装</span>
        </div>
        <el-form label-width="70px">
          <el-form-item label="安装包">
            <el-input type="textarea" v-model="app_path" style="width: 400px" class="form-control"
                      placeholder="输入要安装的app地址,本地地址或网络地址都可以"></el-input>
          </el-form-item>
          <el-form-item label="批量安装">
            <el-switch v-model="all_install" active-text="是"></el-switch>
          </el-form-item>
          <el-form-item>
            <el-button :disabled="installing" type="primary" @click="install">安装</el-button>
          </el-form-item>
        </el-form>
      </el-card>
      <el-card class="box-card" style="margin: 8px">
        <div slot="header" class="clearfix">
          <span>采集设置</span>
        </div>
        <el-form>
          <el-form-item label="采集间隔(秒)">
            <el-input type="number" v-model="interval_time" class="form-control" style="width: 60px"></el-input>
          </el-form-item>
          <el-form-item label="保存详细数据">
            <el-switch v-model="save_detail"></el-switch>
          </el-form-item>
          <el-form-item label="CPU除核数" v-if="platform ==='ios'">
            <el-switch v-model="divided_core_nums"></el-switch>
          </el-form-item>
        </el-form>
      </el-card>
      <el-card class="box-card" style="margin: 8px">
        <div slot="header" class="clearfix">
          <span>其他</span>
        </div>
        <el-form>
          <el-form-item label="图表数据聚合">
            <el-checkbox v-model="dataGroup"></el-checkbox>
          </el-form-item>
          <el-form-item label="图表刷新时间">
            <el-input v-model="refreshTime" type="number" style="width: 100px"></el-input>
          </el-form-item>
          <el-form-item label="采集历史">
            <el-button @click="dialogVisible1 = true;advanced_settting=false">显示</el-button>
          </el-form-item>
        </el-form>
      </el-card>

    </el-drawer>
  </div>
</template>

<script>
import axios from 'axios'
import {getDeviceList, getPackageList, startAPP, installApp, newPerfRecord, updatePerfRecord} from "@/api";
import dataChart from "@/components/dataChart.vue";
import history from "@/components/history.vue";
import bus from "../bus";
const LOCAL_URL = "/"
import Highcharts from 'highcharts'
import stockInit from 'highcharts/modules/stock'
import boostInt from 'highcharts/modules/boost'

Highcharts.setOptions({
  global: {
    useUTC: false
  }
});
stockInit(Highcharts)
boostInt(Highcharts)
export default {
  name: 'yyPerf',
  props: {
    msg: String
  },
  components: {
    dataChart,
    history,
  },
  computed: {
    layoutCss: function () {
      let css = {}
      let number = parseFloat(99 / parseInt(this.layout))
      css['width'] = number.toString() + "%"
      css['height'] = "400px"
      return css
    },
    layoutCss2: function () {
      let css = {}
      let number = parseFloat((window.innerWidth - 100) / parseInt(this.layout))
      css['width'] = number.toString() + "px"
      return css
    },
  },
  data() {
    return {
      refreshTime: 5,
      dataGroup: true,
      recordId: null,
      reloading: false,
      layout: 3,
      installing: false,
      dialogVisible: false,
      dialogVisible1: false,
      startButton: "开始采集",
      direction: 'rtl',
      error: '',
      params: {},
      selected_device: localStorage.selected_device || "",
      platform: 'android',
      device_list: [],
      selected_app: localStorage.selected_app || "",
      package_list: [],
      perf_chart_data: {
        app_cpu: {
          title: "App CPU利用率(%)", label: "app_cpu",
          selected: true, platform: 'android,ios,window', show: false
        },
        total_cpu: {
          title: "整体CPU利用率(%)", label: "total_cpu",
          selected: false, platform: 'android,ios,window', show: false
        },
        memory: {
          title: "内存使用量(MB)", label: "memory",
          selected: true, platform: 'android,ios,window', show: false
        },
        virtual_mem: {
          title: "虚拟内存使用量(MB)", label: "virtual_mem",
          selected: false, platform: 'android', show: false
        },
        threads: {
          title: "线程数", label: "threads",
          selected: true, platform: 'android,ios,window', show: false
        },
        gpu: {
          title: "GPU利用率(%)", label: "gpu",
          selected: true, platform: 'android,ios,window', show: false
        },
        fps: {
          title: "帧率(FPS)", label: "fps",
          selected: false, platform: 'android,ios', show: false
        },
        traffic_down: {
          title: "下行流量(KB)", label: "traffic_down",
          selected: true, platform: 'android,ios,window', show: false
        },
        traffic_up: {
          title: "上行流量(KB)", label: "traffic_up",
          selected: true, platform: 'android,ios,window', show: false
        },
        mediasvrd_cpu: {
          title: "media CPU 占用(%)", label: "mediasvrd_cpu",
          selected: true, platform: 'ios', show: false
        },
        wakeups: {
          title: "唤醒次数", label: "wakeups",
          selected: false, platform: 'android,ios', show: false
        },
        activity: {
          title: "Activities数量", label: "activity",
          selected: false, platform: 'android,ios', show: false
        },
        native_mem: {
          title: "Native使用量(MB)", label: "native_mem",
          selected: false, platform: 'android,ios', show: false
        },
        dalvik_mem: {
          title: "Dalvik使用量(MB)", label: "dalvik_mem",
          selected: false, platform: 'android,ios', show: false
        },
        // rss: {
        //   title: "rss内存(MB)", label: "rss",
        //   show: false, disable: true, selected: true, platform:'android'
        // },
        // gpu_mem: {
        //   title: "GPU 显存使用量(MB)", label: "gpu_mem",
        //   show: false, disable: true
        // },
        // battery: {
        //   title: "battery", label: "battery",
        //   show: false, disable: true, selected: true, platform:'android,ios'
        // },
        // gpu_temperature: {
        //   title: "GPU温度(℃)", label: "gpu_temperature",
        //   show: false, disable: true, selected: true, platform:'android'
        // },
        handle_count: {
          title: "句柄数量", label: "handle_count",
          selected: true, platform: 'window', show: false
        }
      },
      colWidth: {"width": "100%", "height": "300px"},
      echart_object: {},
      echart_show: false,
      is_capture: false,
      capture_time: localStorage.capture_time || 24,
      timer: null,
      perfws: null,
      perf_filepath: null,
      file_name: "",
      interval_time: 2,
      test_time: 0,
      fresh_interval_timer: null,
      fresh_test_timer: null,
      // simple_perf_data: [],
      advanced_settting: false,
      save_detail: localStorage.save_detail || false,
      divided_core_nums: false,
      all_install: localStorage.all_install || false,
      app_path: "",
      getting: false,
      selectData: [],
    }
  },
  watch: {
    platform: function () {
      this.changePlatform()
    },
    selected_device: function (newval) {
      if (this.selected_device.indexOf('iPhone') !== -1 || this.selected_device.indexOf('iOS') !== -1) {
        this.platform = 'ios'
      } else if (this.selected_device.toLowerCase().indexOf("windows") !== -1) {
        this.platform = "windows"
      } else {
        this.platform = 'android'
      }
      localStorage.setItem('platform', this.platform);
      localStorage.setItem('selected_device', newval);
      this.serial = this.selected_device.split('|')[1]
      if (newval) {
        this.getPackageList()
      }
      this.initChartData()
    },
    selected_app: function (newval) {
      if (this.selected_app) {
        localStorage.setItem('selected_app', newval);
        // console.log('selected app is '+newval)
        if (this.package_list.indexOf(this.selected_app) !== -1 && this.platform !== "windows") {
          this.startAPP(false)
        }
        this.echart_show = true
      } else {
        this.echart_show = false
      }
    },
    interval_time: function (newval) {
      this.interval_time = newval
      if (this.interval_time > 0 && this.perfws) {
        let data = {
          platform: this.platform,
          device: this.selected_device,
          package: this.selected_app.toString(),
          action: 'change',
          filename: this.file_name,
          intervaltime: this.interval_time
        }
        this.perfws.send(JSON.stringify(data))
      }
    },
    save_detail: function (newval) {
      localStorage.setItem('save_detail', newval);
    },
    all_install: function (newval) {
      localStorage.setItem('all_install', newval);
    },
    capture_time: function (newval) {
      localStorage.setItem('capture_time', newval);
    },
  },
  created() {
  },
  mounted: function () {
    //var URL = window.URL || window.webkitURL;
    if (this.selected_device.indexOf('iPhone') !== -1 || this.selected_device.indexOf('iOS') !== -1) {
      this.platform = 'ios'
    } else if (this.selected_device.toLowerCase().indexOf("windows") !== -1) {
      this.platform = "windows"
    } else {
      this.platform = 'android'
    }
    this.params = this.GetRequestParam(window.location.search)
    this.platform = this.params['platform'] || this.platform
    this.echart_show = false
    this.divided_core_nums = false

    this.getDeviceList()
    this.getPackageList()
    this.initChartData()
    this.initPerfWebSocket()


  },
  methods: {
    updatePerfRecord() {
      let param = {"end_time": new Date().getTime(), "filepath": this.perf_filepath}
      updatePerfRecord(this.recordId, param).then(ret => {
        console.log(ret)
      }).catch(err => {
        if (axios.isCancel(err)) {
          return
        }
        this.showAjaxError(err);
      })
    },
    newPerfRecord(param) {
      newPerfRecord(param).then(ret => {
        this.recordId = ret.data.id
      }).catch(err => {
        if (axios.isCancel(err)) {
          return
        }
        this.showAjaxError(err);
      })
    },
    changeLayout: function () {
      this.reloading = true
      // 延时一秒后执行
      setTimeout(() => {
        this.reloading = false
        for (let i in this.perf_chart_data) {
          if (this.perf_chart_data[i].selected) {
            if (this.$refs['chart_' + i][0].count > 0) {
              this.$refs['chart_' + i][0].resize()
            }
          }

        }
      }, 500)
    },
    getSelectData: function () {
      let key = []
      for (let i in this.perf_chart_data) {
        if (this.perf_chart_data[i].platform.indexOf(this.platform) !== -1) {
          this.perf_chart_data[i].show = true
          if (this.perf_chart_data[i].selected) {
            key.push(i)
          }
        } else {
          this.perf_chart_data[i].show = false
        }
      }
      return key
    },
    handleShowChange(value) {
      for (let i in this.perf_chart_data) {
        if (value.indexOf(i) !== -1) {
          this.perf_chart_data[i].selected = true
        } else {
          this.perf_chart_data[i].selected = false
        }
      }
    },
    GetRequestParam(url) {
      let params = {};
      if (url.indexOf("?") !== -1) {
        let str = url.substr(1);
        let strlist = str.split("&");
        for (let i = 0; i < strlist.length; i++) {
          params[strlist[i].split("=")[0]] = unescape(strlist[i].split("=")[1]);
        }
      }
      return params;
    },
    setAvgResult: function (row, column) {
      let result = -1
      Object.keys(row).forEach(key => {
        if (row[key].title === column.label) {
          result = this.$refs['chart_' + key][0].avg_result
        }
      })
      return result
    },
    initChartData: function () {
      this.echart_object = {}
      if (this.platform === 'ios') {
        this.perf_chart_data['native_mem'].title = "Real Mem使用量(MB)"
        this.perf_chart_data['dalvik_mem'].title = "Real Private Mem使用量(MB)"
      } else if (this.platform === 'android') {
        this.perf_chart_data['native_mem'].title = "Native使用量(MB)"
        this.perf_chart_data['dalvik_mem'].title = "Dalvik使用量(MB)"
      }
      // this.simple_perf_data = [this.perf_chart_data]
      if (this.selectData.length === 0) {
        this.selectData = this.getSelectData()
      } else {
        for (let i in this.perf_chart_data) {
          if (this.selectData.indexOf(i) === -1) {
            this.perf_chart_data[i].selected = false
          } else {
            this.perf_chart_data[i].selected = true
          }
        }
      }
    },
    changePlatform() {
      this.selectData = this.getSelectData()
    },
    getDeviceList: function () {
      this.getting = true
      getDeviceList().then(ret => {
        this.device_list = ret.data.data;
        for (let index = 0; index < this.device_list.length; index++) {
          let device = this.device_list[index]
          if (device.indexOf(this.params['serial']) !== -1 || device === this.selected_device) {
            this.selected_device = device
            this.getPackageList()
            break
          }
        }
        this.getting = false;
      }).catch(err => {
        if (axios.isCancel(err)) {
          return
        }
        this.getting = false;
        console.log(err)
        this.showAjaxError(err);

      })
    },
    getPackageList: function () {
      if (this.selected_device && this.device_list.indexOf(this.selected_device) !== -1) {
        this.selected_app = "应用列表加载中，请稍后"
        getPackageList(encodeURIComponent(this.selected_device)).then(ret => {
          this.package_list = ret.data.data;
          if (this.package_list.indexOf(this.selected_app) !== -1) {
            this.startAPP(false)
          } else {
            this.selected_app = ""
          }
        }).catch(err => {
          if (axios.isCancel(err)) {
            return
          }
          this.showAjaxError(err);
        })
      } else {
        this.package_list = []
        this.selected_app = "请先选择测试设备"
      }
    },
    startAPP: function (stop = true) {
      if (this.selected_device && this.selected_app && this.platform !== "windows") {
        let data = new FormData();
        data.append("deviceinfo", this.selected_device);
        data.append("package", this.selected_app);
        data.append("stop", stop);
        startAPP(data).then(ret => {
          console.log(ret)
        }).catch(err => {
          if (axios.isCancel(err)) {
            return
          }
          this.showAjaxError(err);
        })
      }
    },
    install: function () {
      if (!this.all_install && !this.selected_device)
        return
      if (this.app_path) {
        this.installing = true
        let param = new FormData();
        param.append("deviceinfo", this.selected_device);
        param.append("all_install", this.all_install);
        param.append("app_path", this.app_path);
        installApp(param).then(ret => {
          this.installing = false
          this.$message.success("安装成功");
        }).catch(err => {
          if (axios.isCancel(err)) {
            return
          }
          this.installing = false
          this.$message.error(err);

        })
      }
    },
    startCapture: function () {
      console.log("startCapture")
      let data = {
        platform: this.platform,
        device: this.selected_device,
        package: this.selected_app.toString(),
        action: 'start',
        filename: this.file_name,
        intervaltime: this.interval_time,
        save_detail: this.save_detail,
        divided_core_nums: this.divided_core_nums,
        capture_time: this.capture_time
      }
      this.perf_filepath = null
      //点击后设置按钮不可用
      document.title = "性能工具-" + this.selected_device
      let param = {"devices": this.selected_device, "app_name": null, "app_version": null, "app_package": null}
      this.echart_show = false
      let temp = this.selected_app.split("--")
      if (temp.length === 2) {
        param['app_name'] = temp[0].split(" ")[0]
        param['app_version'] = temp[0].split(" ")[1]
        param['app_package'] = temp[1]
      }
      if (this.is_capture === false) {
        this.newPerfRecord(param)
        this.clearData()
        this.is_capture = true
        this.initChartData()
        this.startButton = "停止采集"
        if (this.selected_device && this.selected_app) {
          data['action'] = 'start'
        }
        if (this.fresh_interval_timer === null) {
          let _this = this
          this.fresh_interval_timer = setInterval(function () {
            _this.interval_time += 5
            if (_this.interval_time > 120) {
              _this.interval_time = 120
            }
          }, 60 * 60 * 1000)
        }
        if (this.fresh_test_timer === null) {
          let _this = this
          this.fresh_test_timer = setInterval(function () {
            _this.test_time += 1
          }, 60 * 1000)
        }
      } else {
        this.is_capture = false
        this.startButton = "开始采集"
        data['action'] = 'stop'
        this.test_time = 0
        if (this.fresh_interval_timer) {
          clearInterval(this.fresh_interval_timer)
          this.fresh_interval_timer = null
        }
        if (this.fresh_test_timer) {
          clearInterval(this.fresh_test_timer)
          this.fresh_test_timer = null
        }

      }
      if (this.perfws) {
        this.perfws.send(JSON.stringify(data))
      }
    },
    initPerfWebSocket() {
      // 初始化变量
      const ws = this.perfws = new WebSocket("ws://" + location.host + "/ws/v1/captrue")
      // const ws = this.perfws = new WebSocket("ws://127.0.0.1:17310/ws/v1/captrue")
      ws.onopen = () => {
        console.log("websocket opened")
      }
      let that = this
      ws.onmessage = (message) => {
        //数据返回，设置按钮可用
        that.echart_show = true
        const data = JSON.parse(message.data)
        console.log("websocket get new message")
        if (data.hasOwnProperty('filepath')) {
          that.perf_filepath = data['filepath']
          that.updatePerfRecord()
        } else if (data.hasOwnProperty('dumphprof')) {
          document.getElementById("dump_hprof").disabled = false
        } else {
          for (let index = 0; index < data.length; index++) {
            let perfdata = data[index]
            // console.log(perfdata)
            bus.$emit('newData', perfdata);
            // Object.keys(that.perf_chart_data).forEach(key => {
            //   if (that.perf_chart_data[key].show && that.perf_chart_data[key].selected) {
            //     that.$refs['chart_' + key][0].addData(perfdata)
            //   }
            // })
          }
        }
      }
      ws.onclose = () => {
        that.perfws = null
        console.log("websocket closed")
      }
    },

    dumpHprof: function () {
      if (this.selected_device && this.selected_app && this.is_capture && this.perfws) {
        document.getElementById("dump_hprof").disabled = true
        let data = {
          platform: this.platform,
          device: this.selected_device,
          package: this.selected_app.toString(),
          action: 'dumphprof',
          filename: this.file_name,
          intervaltime: this.interval_time
        }
        this.perfws.send(JSON.stringify(data))
      }
    },

    exportData: function () {
      this.dialogVisible = false
      if (this.perf_filepath) {
        let url = LOCAL_URL + "api/v1/export/" + encodeURIComponent(this.perf_filepath) + "/" + encodeURIComponent(this.file_name)
        window.open(url)
      }
    },
    clearData: function () {
      this.echart_show = true;
      // this.perf_chart_data = {}
      this.is_capture = false
      this.test_time = 0
      for (let i in this.perf_chart_data) {
        if (this.perf_chart_data[i].show && this.perf_chart_data[i].selected && this.$refs['chart_' + i][0] && this.$refs['chart_' + i][0].count > 0) {
          this.$refs['chart_' + i][0].clearData()
        }
      }
      this.initChartData()
    },
    dateFormat: function (fmt, date) {
      let ret
      const opt = {
        "Y+": date.getFullYear().toString(),        // 年
        "m+": (date.getMonth() + 1).toString(),     // 月
        "d+": date.getDate().toString(),            // 日
        "H+": date.getHours().toString(),           // 时
        "M+": date.getMinutes().toString(),         // 分
        "S+": date.getSeconds().toString()          // 秒
        // 有其他格式化字符需求可以继续添加，必须转化成字符串
      }
      for (let k in opt) {
        ret = new RegExp("(" + k + ")").exec(fmt);
        if (ret) {
          fmt = fmt.replace(ret[1], (ret[1].length == 1) ? (opt[k]) : (opt[k].padStart(ret[1].length, "0")))
        }
      }
      return fmt
    },
    showError: function (error) {
      this.loading = false;
      this.error = error;
      this.$message({
        message: this.error,
        type: 'warning'
      });
    },
    showAjaxError: function (ret) {
      if (ret.responseJSON && ret.responseJSON.description) {
        this.showError(ret.responseJSON.description);
      } else {
        this.showError("<p>Local server not started, start with</p><pre>$ python -m weditor</pre>");
      }
    },
  }
}
</script>
<style scoped>
.filter {
  padding: 10px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}
</style>
