<template>
  <div>
    <div v-show="count>0" @mouseover="handleMouseOver" @mouseout="handleMouseOut">
      <!--    <highcharts :options="chartOption" :constructor-type="'stockChart'" ref="chart"-->
      <!--                :updateArgs="[false, true, true]"-->
      <!--    ></highcharts>-->
      <div ref="chart"></div>
    </div>
    <div v-show="count===0">
      <el-empty :description="'暂无'+title+'数据'"></el-empty>
    </div>
  </div>
</template>
<script>
import Highcharts from 'highcharts/highstock';
import stockInit from 'highcharts/modules/stock'
import bus from "../bus";

Highcharts.setOptions({
  global: {
    useUTC: false
  }
});
stockInit(Highcharts)
export default {
  name: 'dataChart',
  props: {
    title: {
      type: String,
      default: ''
    },
    refreshTime: {
      type: Number,
      default: 5,
    },
    label: {
      type: String,
      default: ''
    },
    dataGroup: {
      type: Boolean,
      default: true,
    },
    capture:{
      type: Boolean,
      default: true,
    },
    multiple: {
      type: Boolean,
      default: false,
    },
  },
  // components: {
  //   'highcharts': Chart,
  // },
  data() {
    return {
      chart: null,
      isActive: true, // 初始化为活动状态
      timer: null,
      refresh: true,
      avg_result: "-1",
      sum: 0,
      count: 0,
      chartOption: {
        global: {
          useUTC: false
        },
        rangeSelector: {
          buttons: [],
          inputEnabled: false,
        },
        chart: {
          zoomType: '',
          width: null,
          zooming: {
            mouseWheel: {
              enabled: false
            }
          },
        },
        navigator: {
          enabled: false
        },
        tooltip: {
          shared: true // 开启交叉显示多条曲线的数据
        },
        credits: {
          enabled: false
        },
        title: {
          text: this.title
        },
        // yAxis: {
        //   title: {
        //     text: this.label
        //   },
        //   opposite: false,
        // },
        exporting: {
          enabled: false
        },
        legend: false,
        plotOptions: {
          series: {
            dataGrouping: {
              approximation: 'average',
              units: [[
                'minute',
                [1]
              ]]
            }
          }
        },
        series: [
          {
            name: this.title,
            type: "spline",
            data: [],
            events: {},
            tooltip: {
              shared: false, // 不共享提示框
              hideDelay: 1000, // 增加提示框隐藏延迟
              pointFormat: '{point.series.name}:{point.y}'
            },
          }
        ]
      }
    }
  },
  methods: {
    handleMouseOver() {
      // 打印显示那个图表获取鼠标焦点了
      console.log(this.title + "获取鼠标焦点了")
      if (this.timer !== null) {
        // 打印显示那个图表被暂停了
        console.log(this.title + "被暂停了")
        clearInterval(this.timer)
        this.timer = null
      }
    },
    handleMouseOut() {
      // 打印显示那个图表失去鼠标焦点了
      console.log(this.title + "失去鼠标焦点了")
      if (this.timer === null) {
        // 打印显示那个图表被恢复了
        console.log(this.title + "被恢复了")
        this.timer = setInterval(this.redraw, this.refreshTime * 1000)
      }
    },
    clearData() {
      this.sum = 0;
      this.avg_result = "-1"
      this.count = 0
      for (let i in this.chartOption.series) {
        this.chartOption.series[i].data = []
      }
    },
    redraw() {
      if (this.count > 1) {
        // 打印日志输出那个图表被刷新了
        console.log(this.title + "被刷新了")
        this.chart.redraw();
      }
    },
    resize() {
      this.chart.setSize(null, null)
    },
    handleVisibilityChange() {
      // 当页面可见性状态发生变化时触发
      if (document.hidden) {
        this.isActive = false; // 页面不可见
      } else {
        this.isActive = true; // 页面可见
      }
    },
    addData(data) {
      let key = this.label.split(",")
      let title = this.title.split(",")
      if (key.length === 2) {
        this.chartOption.series.push(
            {
              name: this.title,
              type: "spline",
              data: [],
              tooltip: {
                shared: false, // 不共享提示框
                hideDelay: 1000, // 增加提示框隐藏延迟
                pointFormat: '{point.series.name}:{point.y}'
              },
            }
        )
      }
      for (let i in key) {
        let value = parseFloat(data[key[i]])
        let time = (new Date()).getTime()
        this.chart.series[0].addPoint([time, value], false, false);
        this.count += 1
        this.chartOption.series[i].name = title[i]
        this.sum += value
        this.avg_result = (this.sum / this.count).toFixed(2)
      }

    }
  },
  watch: {
    refreshTime: function (newVal) {
      if (newVal) {
        clearInterval(this.timer)
        this.timer = setInterval(this.redraw, this.refreshTime * 1000)
      }
    },
    capture: function (newVal) {
      if (!newVal) {
        clearInterval(this.timer)
      }
    },
    dataGroup: function (newVal) {
      if (newVal) {
        this.chartOption.plotOptions.series = {
          dataGrouping: {
            approximation: 'average',
            units: [[
              'minute',
              [1]
            ]]
          },
        }
        this.chart = Highcharts.stockChart(this.$refs.chart, this.chartOption);
      } else {
        this.chartOption.plotOptions.series = {}
        this.chart = Highcharts.stockChart(this.$refs.chart, this.chartOption);
      }
    },
    isActive: function (newVal) {
      if (newVal) {
        clearInterval(this.timer)
        this.timer = setInterval(this.redraw, this.refreshTime * 1000)
      } else {
        clearInterval(this.timer)
        this.timer = setInterval(this.redraw, 10 * this.refreshTime * 1000)
      }
    },
  },
  created() {
    bus.$on('newData', msg => {
      this.addData(msg)
    });
  },
  mounted() {
    this.chart = Highcharts.stockChart(this.$refs.chart, this.chartOption);
    this.timer = setInterval(this.redraw, this.refreshTime * 1000)
    document.addEventListener('visibilitychange', this.handleVisibilityChange);
  },
  beforeDestroy() {
    bus.$off("newData")
    document.removeEventListener('visibilitychange', this.handleVisibilityChange);
    clearInterval(this.timer)
  }

}

</script>
<style scoped>

</style>