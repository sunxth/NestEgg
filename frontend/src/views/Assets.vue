<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">资产管理</h1>
      <button v-if="authStore.isAdmin"
              @click="showAddAssetModal = true"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700">
        添加资产
      </button>
    </div>

    <!-- 资产概览 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-gradient-to-r from-green-500 to-green-600 p-4 rounded-lg shadow text-white">
        <dt class="text-sm font-medium text-green-100">总资产</dt>
        <dd class="mt-1 text-3xl font-bold">
          ¥{{ totalAssets.toFixed(2) }}
        </dd>
        <p class="text-xs text-green-100 mt-1">含资金池余额</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <dt class="text-sm font-medium text-gray-500">流动资产</dt>
        <dd class="mt-1 text-2xl font-semibold text-blue-600">
          ¥{{ liquidAssets.toFixed(2) }}
        </dd>
        <p class="text-xs text-gray-500 mt-1">{{ ((liquidAssets / totalAssets) * 100).toFixed(1) }}%</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <dt class="text-sm font-medium text-gray-500">固定资产</dt>
        <dd class="mt-1 text-2xl font-semibold text-indigo-600">
          ¥{{ fixedAssets.toFixed(2) }}
        </dd>
        <p class="text-xs text-gray-500 mt-1">{{ ((fixedAssets / totalAssets) * 100).toFixed(1) }}%</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <dt class="text-sm font-medium text-gray-500">投资资产</dt>
        <dd class="mt-1 text-2xl font-semibold text-purple-600">
          ¥{{ investmentAssets.toFixed(2) }}
        </dd>
        <p class="text-xs text-gray-500 mt-1">{{ ((investmentAssets / totalAssets) * 100).toFixed(1) }}%</p>
      </div>
    </div>

    <!-- 资产分布图表 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-lg font-medium text-gray-900 mb-4">资产分布</h2>
        <div class="h-64">
          <Doughnut v-if="assetDistributionData" :data="assetDistributionData" :options="pieChartOptions" />
        </div>
      </div>
      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-lg font-medium text-gray-900 mb-4">资产趋势</h2>
        <div class="h-64">
          <Line v-if="assetTrendData" :data="assetTrendData" :options="lineChartOptions" />
        </div>
      </div>
    </div>

    <!-- 资产列表 -->
    <div class="bg-white shadow rounded-lg overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-lg font-medium text-gray-900">资产明细</h2>
      </div>

      <!-- 流动资产 -->
      <div class="border-b border-gray-200">
        <div class="bg-blue-50 px-6 py-3">
          <h3 class="text-sm font-medium text-blue-900">流动资产</h3>
        </div>
        <ul class="divide-y divide-gray-200">
          <li class="px-6 py-4 hover:bg-gray-50 flex justify-between items-center">
            <div>
              <p class="text-sm font-medium text-gray-900">资金池余额</p>
              <p class="text-xs text-gray-500">现金及现金等价物</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-semibold text-gray-900">¥{{ fundPoolBalance.toFixed(2) }}</p>
              <p class="text-xs text-gray-500">自动更新</p>
            </div>
          </li>
          <li v-for="asset in liquidAssetsList" :key="asset.id"
              class="px-6 py-4 hover:bg-gray-50 flex justify-between items-center">
            <div>
              <p class="text-sm font-medium text-gray-900">{{ asset.name }}</p>
              <p class="text-xs text-gray-500">{{ asset.description }}</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-semibold text-gray-900">¥{{ asset.amount.toFixed(2) }}</p>
              <div class="flex items-center gap-2 justify-end">
                <p class="text-xs text-gray-500">{{ formatDate(asset.updateDate) }}</p>
                <button v-if="authStore.isAdmin" @click="editAsset(asset)"
                        class="text-xs text-indigo-600 hover:text-indigo-900">编辑</button>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- 固定资产 -->
      <div class="border-b border-gray-200">
        <div class="bg-indigo-50 px-6 py-3">
          <h3 class="text-sm font-medium text-indigo-900">固定资产</h3>
        </div>
        <ul class="divide-y divide-gray-200">
          <li v-for="asset in fixedAssetsList" :key="asset.id"
              class="px-6 py-4 hover:bg-gray-50 flex justify-between items-center">
            <div>
              <p class="text-sm font-medium text-gray-900">{{ asset.name }}</p>
              <p class="text-xs text-gray-500">{{ asset.description }}</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-semibold text-gray-900">¥{{ asset.amount.toFixed(2) }}</p>
              <div class="flex items-center gap-2 justify-end">
                <p class="text-xs text-gray-500">{{ formatDate(asset.updateDate) }}</p>
                <button v-if="authStore.isAdmin" @click="editAsset(asset)"
                        class="text-xs text-indigo-600 hover:text-indigo-900">编辑</button>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- 投资资产 -->
      <div>
        <div class="bg-purple-50 px-6 py-3">
          <h3 class="text-sm font-medium text-purple-900">投资资产</h3>
        </div>
        <ul class="divide-y divide-gray-200">
          <li v-for="asset in investmentAssetsList" :key="asset.id"
              class="px-6 py-4 hover:bg-gray-50 flex justify-between items-center">
            <div>
              <p class="text-sm font-medium text-gray-900">{{ asset.name }}</p>
              <p class="text-xs text-gray-500">{{ asset.description }}</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-semibold text-gray-900">¥{{ asset.amount.toFixed(2) }}</p>
              <div class="flex items-center gap-2 justify-end">
                <span v-if="asset.changeRate"
                      class="text-xs"
                      :class="asset.changeRate >= 0 ? 'text-green-600' : 'text-red-600'">
                  {{ asset.changeRate >= 0 ? '+' : '' }}{{ asset.changeRate.toFixed(2) }}%
                </span>
                <p class="text-xs text-gray-500">{{ formatDate(asset.updateDate) }}</p>
                <button v-if="authStore.isAdmin" @click="editAsset(asset)"
                        class="text-xs text-indigo-600 hover:text-indigo-900">编辑</button>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Doughnut, Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { useAuthStore } from '@/stores/auth'
import axios from '@/utils/axios'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

const authStore = useAuthStore()

const showAddAssetModal = ref(false)
const fundPoolBalance = ref(0)

// 模拟资产数据
const liquidAssetsList = ref([
  { id: 1, name: '活期存款', amount: 50000, description: '工商银行', updateDate: new Date() },
  { id: 2, name: '余额宝', amount: 10000, description: '支付宝', updateDate: new Date() }
])

const fixedAssetsList = ref([
  { id: 3, name: '定期存款', amount: 100000, description: '一年期 3.5%', updateDate: new Date() },
  { id: 4, name: '国债', amount: 50000, description: '三年期', updateDate: new Date() }
])

const investmentAssetsList = ref([
  { id: 5, name: '股票基金', amount: 30000, description: '易方达蓝筹', changeRate: 5.2, updateDate: new Date() },
  { id: 6, name: '债券基金', amount: 20000, description: '鹏华债券', changeRate: 2.3, updateDate: new Date() }
])

const totalAssets = computed(() => {
  const liquid = liquidAssets.value
  const fixed = fixedAssets.value
  const investment = investmentAssets.value
  return liquid + fixed + investment
})

const liquidAssets = computed(() => {
  const sum = liquidAssetsList.value.reduce((acc, asset) => acc + asset.amount, 0)
  return fundPoolBalance.value + sum
})

const fixedAssets = computed(() => {
  return fixedAssetsList.value.reduce((acc, asset) => acc + asset.amount, 0)
})

const investmentAssets = computed(() => {
  return investmentAssetsList.value.reduce((acc, asset) => acc + asset.amount, 0)
})

const assetDistributionData = computed(() => ({
  labels: ['流动资产', '固定资产', '投资资产'],
  datasets: [{
    data: [liquidAssets.value, fixedAssets.value, investmentAssets.value],
    backgroundColor: [
      'rgba(59, 130, 246, 0.8)',
      'rgba(99, 102, 241, 0.8)',
      'rgba(139, 92, 246, 0.8)'
    ]
  }]
}))

const assetTrendData = ref({
  labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
  datasets: [{
    label: '总资产',
    data: [280000, 285000, 290000, 288000, 295000, 300000],
    borderColor: 'rgb(34, 197, 94)',
    backgroundColor: 'rgba(34, 197, 94, 0.1)',
    tension: 0.3,
    fill: true
  }]
})

const pieChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right'
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const label = context.label || ''
          const value = context.parsed
          const total = context.dataset.data.reduce((a, b) => a + b, 0)
          const percentage = ((value / total) * 100).toFixed(1)
          return `${label}: ¥${value.toFixed(2)} (${percentage}%)`
        }
      }
    }
  }
}

const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: false,
      ticks: {
        callback: (value) => `¥${value / 10000}万`
      }
    }
  }
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('zh-CN')
}

function editAsset(asset) {
  console.log('Edit asset:', asset)
}

async function loadFundPoolBalance() {
  try {
    const response = await axios.get('/api/fund-pool/')
    fundPoolBalance.value = parseFloat(response.data.current_balance)
    console.log('Fund pool balance loaded:', response.data.current_balance)
  } catch (error) {
    console.error('Failed to load fund pool balance:', error)
    // 如果失败，设置默认值
    fundPoolBalance.value = 47830
  }
}

onMounted(() => {
  loadFundPoolBalance()
})
</script>