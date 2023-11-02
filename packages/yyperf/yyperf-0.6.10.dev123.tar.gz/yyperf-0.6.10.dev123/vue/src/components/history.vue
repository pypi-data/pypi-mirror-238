<template>
  <div>
    <el-form :inline="true">
      <el-form-item>
        <el-input v-model="search" style="width: 400px" placeholder="模糊搜索" @change="getPerfDataList"></el-input>
      </el-form-item>
    </el-form>
    <el-table :data="dataList">
      <!-- 展示PerfDataRecord 属性  -->
      <el-table-column prop="start_time" label="创建时间"></el-table-column>
      <el-table-column prop="end_time" label="更新时间"></el-table-column>
      <el-table-column prop="duration" label="采集时间(分钟)"></el-table-column>
      <el-table-column prop="devices" label="设备"></el-table-column>
      <el-table-column prop="app_name" label="APP名称"></el-table-column>
      <el-table-column prop="app_version" label="APP版本"></el-table-column>
      <el-table-column prop="app_package" label="APP包名"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" @click="exportData(scope.row)">导出
          </el-button>
          <el-button type="danger" size="mini" @click="deletePerfRecord(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div style="text-align: center;margin-top: 10px;">
      <el-pagination layout="prev, pager, next" :total="total" :page-size="page_size" :current-page.sync="page"
                     @current-change="changeCurrentPage">
      </el-pagination>
    </div>
  </div>
</template>
<script>
import {getPerfDataList, deletePerfRecord} from "@/api";
const LOCAL_URL = "/"
export default {
  name: "history",
  data() {
    return {
      total: 1,
      search:"",
      dataList: [],
      page: 1,
      page_size: 10,
    }
  }, mounted() {
    this.getPerfDataList()
  },
  methods: {
    changeCurrentPage() {
      this.getPerfDataList()
    },
    exportData: function (row) {
      console.log(row)
      if (row.filepath) {
        let url = LOCAL_URL + "api/v1/export/" + encodeURIComponent(row.filepath) + "/"
        window.open(url)
      }else {
        this.$message.error("没有数据")
      }
    },
    getPerfDataList() {
      let param = {
        page: this.page,
        page_size: this.page_size,
      }
      if(this.search !== ""){
        param.search = this.search
      }
      getPerfDataList(param).then(res => {
        this.total = res.data.total_records
        this.dataList = res.data.data
      })
    },
    deletePerfRecord(id) {
      deletePerfRecord(id).then(res => {
        this.getPerfDataList()
      })
    }
  }
}
</script>
<style>

</style>