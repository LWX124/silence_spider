<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon accounts">
              <el-icon><UserFilled /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ stats.accounts }}</div>
              <div class="stats-label">公众号总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon articles">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ stats.articles }}</div>
              <div class="stats-label">文章总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon tasks">
              <el-icon><List /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ stats.tasks }}</div>
              <div class="stats-label">任务总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon proxies">
              <el-icon><Connection /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ stats.proxies }}</div>
              <div class="stats-label">代理总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>文章采集趋势</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="articleChartOption" style="height: 300px" />
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>任务执行状态</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="taskChartOption" style="height: 300px" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近活动 -->
    <el-row :gutter="20" class="activity-row">
      <el-col :span="12">
        <el-card class="activity-card">
          <template #header>
            <div class="card-header">
              <span>最近任务</span>
              <el-button type="text" @click="viewAllTasks">查看全部</el-button>
            </div>
          </template>
          <div class="activity-list">
            <div
              v-for="task in recentTasks"
              :key="task.id"
              class="activity-item"
            >
              <div class="activity-icon">
                <el-icon><List /></el-icon>
              </div>
              <div class="activity-content">
                <div class="activity-title">{{ task.name }}</div>
                <div class="activity-time">{{ task.created_at }}</div>
              </div>
              <div class="activity-status">
                <el-tag :type="getTaskStatusType(task.status)">
                  {{ task.status }}
                </el-tag>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="activity-card">
          <template #header>
            <div class="card-header">
              <span>系统状态</span>
            </div>
          </template>
          <div class="system-status">
            <div class="status-item">
              <span class="status-label">CPU使用率</span>
              <el-progress :percentage="systemStatus.cpu" />
            </div>
            <div class="status-item">
              <span class="status-label">内存使用率</span>
              <el-progress :percentage="systemStatus.memory" />
            </div>
            <div class="status-item">
              <span class="status-label">磁盘使用率</span>
              <el-progress :percentage="systemStatus.disk" />
            </div>
            <div class="status-item">
              <span class="status-label">网络状态</span>
              <el-tag type="success">正常</el-tag>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import VChart from 'vue-echarts'

// 注册ECharts组件
use([
  CanvasRenderer,
  LineChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

const router = useRouter()

// 响应式数据
const stats = ref({
  accounts: 156,
  articles: 2847,
  tasks: 89,
  proxies: 23
})

const systemStatus = ref({
  cpu: 45,
  memory: 62,
  disk: 78
})

const recentTasks = ref([
  {
    id: 1,
    name: '采集公众号：科技前沿',
    status: 'completed',
    created_at: '2024-01-15 14:30'
  },
  {
    id: 2,
    name: '更新文章阅读数据',
    status: 'running',
    created_at: '2024-01-15 13:45'
  },
  {
    id: 3,
    name: '导出数据报告',
    status: 'pending',
    created_at: '2024-01-15 12:20'
  }
])

// 图表配置
const articleChartOption = ref({
  title: {
    text: '文章采集趋势',
    left: 'center'
  },
  tooltip: {
    trigger: 'axis'
  },
  xAxis: {
    type: 'category',
    data: ['1月', '2月', '3月', '4月', '5月', '6月']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '采集文章数',
      type: 'line',
      data: [120, 200, 150, 80, 70, 110],
      smooth: true
    }
  ]
})

const taskChartOption = ref({
  title: {
    text: '任务执行状态',
    left: 'center'
  },
  tooltip: {
    trigger: 'item'
  },
  series: [
    {
      name: '任务状态',
      type: 'pie',
      radius: '50%',
      data: [
        { value: 45, name: '已完成' },
        { value: 15, name: '执行中' },
        { value: 20, name: '等待中' },
        { value: 9, name: '失败' }
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
})

// 方法
const getTaskStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    completed: 'success',
    running: 'warning',
    pending: 'info',
    failed: 'danger'
  }
  return statusMap[status] || 'info'
}

const viewAllTasks = () => {
  router.push('/tasks')
}

// 生命周期
onMounted(() => {
  // 加载数据
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stats-card {
  height: 120px;
}

.stats-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stats-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  font-size: 24px;
  color: #fff;
}

.stats-icon.accounts {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stats-icon.articles {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stats-icon.tasks {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stats-icon.proxies {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stats-number {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 4px;
}

.stats-label {
  font-size: 14px;
  color: #666;
}

.charts-row {
  margin-bottom: 20px;
}

.chart-card {
  height: 400px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  height: 300px;
}

.activity-row {
  margin-bottom: 20px;
}

.activity-card {
  height: 400px;
}

.activity-list {
  max-height: 300px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 40px;
  height: 40px;
  background: #f5f5f5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  color: #666;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 14px;
  color: #333;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: #999;
}

.system-status {
  padding: 20px 0;
}

.status-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.status-label {
  width: 100px;
  font-size: 14px;
  color: #333;
  margin-right: 20px;
}

.status-item .el-progress {
  flex: 1;
}
</style> 