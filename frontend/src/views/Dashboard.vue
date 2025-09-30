<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- 页面标题和日期 -->
      <div class="mb-6">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-semibold text-gray-900">财务概览</h1>
          <div class="relative">
            <button @click="showDatePicker = !showDatePicker"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors">
              {{ currentMonth }}
              <svg class="inline-block w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <!-- 日期选择下拉菜单 -->
            <div v-if="showDatePicker"
                 class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
              <div class="p-2">
                <button @click="selectPeriod('thisWeek')"
                        :class="selectedPeriod === 'thisWeek' ? 'bg-indigo-50 text-indigo-700' : 'text-gray-700 hover:bg-gray-50'"
                        class="w-full text-left px-3 py-2 text-sm rounded transition-colors">
                  本周
                </button>
                <button @click="selectPeriod('current')"
                        :class="selectedPeriod === 'current' ? 'bg-indigo-50 text-indigo-700' : 'text-gray-700 hover:bg-gray-50'"
                        class="w-full text-left px-3 py-2 text-sm rounded transition-colors">
                  本月
                </button>
                <button @click="selectPeriod('lastMonth')"
                        :class="selectedPeriod === 'lastMonth' ? 'bg-indigo-50 text-indigo-700' : 'text-gray-700 hover:bg-gray-50'"
                        class="w-full text-left px-3 py-2 text-sm rounded transition-colors">
                  上月
                </button>
                <button @click="selectPeriod('thisYear')"
                        :class="selectedPeriod === 'thisYear' ? 'bg-indigo-50 text-indigo-700' : 'text-gray-700 hover:bg-gray-50'"
                        class="w-full text-left px-3 py-2 text-sm rounded transition-colors">
                  今年
                </button>
                <div class="border-t border-gray-100 my-2"></div>
                <div class="px-3 py-2">
                  <label class="block text-xs text-gray-500 mb-1">选择月份</label>
                  <input type="month"
                         v-model="customMonth"
                         @change="selectCustomMonth"
                         class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 核心指标区 - 两大指标横向排列 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <!-- 净收入 -->
        <div class="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
          <div class="mb-2">
            <span class="text-sm text-gray-500">{{ periodLabel }}净收入</span>
          </div>
          <p class="text-2xl font-bold" :class="monthlyNet >= 0 ? 'text-gray-900' : 'text-red-600'">
            {{ monthlyNet >= 0 ? '+' : '-' }}¥{{ Math.abs(monthlyNet).toFixed(0) }}
          </p>
          <div class="flex items-center gap-4 mt-1">
            <span class="text-xs text-gray-500">
              收入 ¥{{ monthlyIncome.toFixed(0) }}
            </span>
            <span class="text-xs text-gray-500">
              支出 ¥{{ monthlyExpense.toFixed(0) }}
            </span>
          </div>
        </div>

        <!-- 储蓄率 -->
        <div class="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
          <div class="mb-2">
            <span class="text-sm text-gray-500">储蓄率</span>
          </div>
          <div class="flex items-center justify-between">
            <p class="text-2xl font-bold text-gray-900">{{ savingRate.toFixed(0) }}%</p>
            <div class="flex-1 max-w-[100px] ml-4">
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="h-2 rounded-full transition-all duration-500"
                     :class="savingRate >= 30 ? 'bg-green-500' : savingRate >= 10 ? 'bg-yellow-500' : 'bg-red-500'"
                     :style="{width: `${Math.min(savingRate, 100)}%`}"></div>
              </div>
            </div>
          </div>
          <p class="text-xs text-gray-500 mt-1">
            {{ savingRate >= 30 ? '优秀' : savingRate >= 10 ? '良好' : '需要改善' }}
          </p>
        </div>
      </div>

      <!-- 资产和流动性区 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- 资金池余额 -->
        <div class="bg-white rounded-xl shadow-sm overflow-hidden">
          <div class="bg-gradient-to-r from-indigo-500 to-indigo-600 px-6 py-4">
            <h3 class="text-white text-sm font-medium mb-2">资金池余额</h3>
            <p class="text-3xl font-bold text-white">
              ¥{{ fundPool?.current_balance?.toFixed(2) || '0.00' }}
            </p>
          </div>
          <div class="px-6 py-4">
            <div class="grid grid-cols-3 gap-4 text-center">
              <div>
                <p class="text-xs text-gray-500">初始资金</p>
                <p class="text-sm font-semibold text-gray-900">¥{{ (fundPool?.initial_amount || 0).toFixed(0) }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500">累计收入</p>
                <p class="text-sm font-semibold text-green-600">+¥{{ (fundPool?.total_income || 0).toFixed(0) }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500">累计支出</p>
                <p class="text-sm font-semibold text-red-600">-¥{{ (fundPool?.total_expenses || 0).toFixed(0) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 收支对比 -->
        <div class="bg-white rounded-xl p-6 shadow-sm">
          <h3 class="text-sm font-medium text-gray-900 mb-4">{{ periodLabel }}收支</h3>
          <div class="space-y-4">
            <!-- 收入条 -->
            <div>
              <div class="flex justify-between items-center mb-1">
                <span class="text-sm text-gray-600">收入</span>
                <span class="text-sm font-semibold text-gray-900">¥{{ monthlyIncome.toFixed(2) }}</span>
              </div>
              <div class="w-full bg-gray-100 rounded-full h-2">
                <div class="bg-green-500 h-2 rounded-full transition-all duration-500"
                     :style="{width: `${getPercentage(monthlyIncome, Math.max(monthlyIncome, monthlyExpense))}%`}"></div>
              </div>
            </div>
            <!-- 支出条 -->
            <div>
              <div class="flex justify-between items-center mb-1">
                <span class="text-sm text-gray-600">支出</span>
                <span class="text-sm font-semibold text-gray-900">¥{{ monthlyExpense.toFixed(2) }}</span>
              </div>
              <div class="w-full bg-gray-100 rounded-full h-2">
                <div class="bg-red-500 h-2 rounded-full transition-all duration-500"
                     :style="{width: `${getPercentage(monthlyExpense, Math.max(monthlyIncome, monthlyExpense))}%`}"></div>
              </div>
            </div>
            <!-- 结余 -->
            <div class="pt-3 border-t border-gray-100">
              <div class="flex justify-between items-center">
                <span class="text-sm font-medium text-gray-600">结余</span>
                <span class="text-lg font-bold" :class="monthlyNet >= 0 ? 'text-indigo-600' : 'text-red-600'">
                  {{ monthlyNet >= 0 ? '+' : '-' }}¥{{ Math.abs(monthlyNet).toFixed(2) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 趋势和分析区 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- 支出趋势 -->
        <div class="bg-white rounded-xl p-6 shadow-sm">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-sm font-medium text-gray-900">支出趋势</h3>
            <div class="flex gap-1">
              <button @click="trendPeriod = '7d'"
                      :class="trendPeriod === '7d' ? 'bg-gray-200 text-gray-900' : 'text-gray-500'"
                      class="px-2 py-1 text-xs rounded transition-colors">
                7天
              </button>
              <button @click="trendPeriod = '30d'"
                      :class="trendPeriod === '30d' ? 'bg-gray-200 text-gray-900' : 'text-gray-500'"
                      class="px-2 py-1 text-xs rounded transition-colors">
                30天
              </button>
            </div>
          </div>
          <div class="h-48">
            <Line v-if="expenseTrendData && hasExpenseData" :data="expenseTrendData" :options="chartOptions" />
            <div v-else class="h-full flex items-center justify-center text-gray-400">
              <div class="text-center">
                <svg class="w-16 h-16 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <p class="text-sm">暂无支出数据</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 支出分类 -->
        <div class="bg-white rounded-xl p-6 shadow-sm">
          <h3 class="text-sm font-medium text-gray-900 mb-4">支出分类</h3>
          <div class="h-48">
            <Doughnut v-if="categoryData && hasCategoryData" :data="categoryData" :options="pieOptions" />
            <div v-else class="h-full flex items-center justify-center text-gray-400">
              <div class="text-center">
                <svg class="w-16 h-16 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                        d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                        d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
                </svg>
                <p class="text-sm">暂无分类数据</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 快捷数据区 - 可折叠 -->
      <div class="mb-8">
        <button @click="showQuickStats = !showQuickStats"
                class="flex items-center gap-2 mb-4 text-sm text-gray-600 hover:text-gray-900 transition-colors">
          <svg class="w-4 h-4 transition-transform" :class="showQuickStats ? 'rotate-90' : ''"
               fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
          快捷统计
        </button>

        <div v-show="showQuickStats" class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-white rounded-xl p-4 shadow-sm">
            <p class="text-xs text-gray-500 mb-1">今日支出</p>
            <p class="text-lg font-semibold text-gray-900">¥{{ todayExpense.toFixed(0) }}</p>
          </div>
          <div class="bg-white rounded-xl p-4 shadow-sm">
            <p class="text-xs text-gray-500 mb-1">本周支出</p>
            <p class="text-lg font-semibold text-gray-900">¥{{ weeklyExpense.toFixed(0) }}</p>
          </div>
          <div class="bg-white rounded-xl p-4 shadow-sm">
            <p class="text-xs text-gray-500 mb-1">交易笔数</p>
            <p class="text-lg font-semibold text-gray-900">{{ transactionCount }}</p>
          </div>
          <div class="bg-white rounded-xl p-4 shadow-sm">
            <p class="text-xs text-gray-500 mb-1">日均支出</p>
            <p class="text-lg font-semibold text-gray-900">¥{{ dailyAverage.toFixed(0) }}</p>
          </div>
        </div>
      </div>

      <!-- 最近交易 -->
      <div class="bg-white rounded-xl shadow-sm">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
          <h3 class="text-sm font-medium text-gray-900">最近交易</h3>
          <router-link to="/transactions" class="text-xs text-indigo-600 hover:text-indigo-700">
            查看全部 →
          </router-link>
        </div>
        <div class="divide-y divide-gray-100">
          <div v-for="transaction in recentTransactions" :key="transaction.id"
               class="px-6 py-3 hover:bg-gray-50 transition-colors">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full flex items-center justify-center"
                     :class="transaction.type === 'income' ? 'bg-green-100' : 'bg-red-100'">
                  <span class="text-xs font-medium"
                        :class="transaction.type === 'income' ? 'text-green-700' : 'text-red-700'">
                    {{ transaction.type === 'income' ? '+' : '-' }}
                  </span>
                </div>
                <div>
                  <p class="text-sm text-gray-900">{{ transaction.description || getCategoryLabel(transaction.category) }}</p>
                  <p class="text-xs text-gray-500">{{ formatDate(transaction.date) }} · {{ getCategoryLabel(transaction.category) }}</p>
                </div>
              </div>
              <p class="text-sm font-medium"
                 :class="transaction.type === 'income' ? 'text-green-600' : 'text-red-600'">
                {{ transaction.type === 'income' ? '+' : '-' }}¥{{ parseFloat(transaction.amount).toFixed(2) }}
              </p>
            </div>
          </div>
          <div v-if="recentTransactions.length === 0" class="px-6 py-12 text-center text-gray-400">
            <p class="text-sm">暂无交易记录</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 悬浮快速记账按钮 (FAB) -->
    <button v-if="authStore.isAdmin"
            @click="showAddModal = true"
            class="fixed bottom-6 right-6 w-14 h-14 bg-indigo-600 text-white rounded-full shadow-lg hover:bg-indigo-700 hover:shadow-xl transition-all duration-200 flex items-center justify-center group z-40">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
      </svg>
      <span class="absolute right-16 bg-gray-900 text-white px-2 py-1 rounded text-xs whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
        快速记账
      </span>
    </button>

    <!-- 记账弹窗 -->
    <AddTransactionModal
      v-if="showAddModal"
      @close="showAddModal = false"
      @success="handleAddSuccess"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useTransactionStore } from '@/stores/transaction'
import { useAuthStore } from '@/stores/auth'
import { Line, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import AddTransactionModal from '@/components/AddTransactionModal.vue'
import axios from '@/utils/axios'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const transactionStore = useTransactionStore()
const authStore = useAuthStore()

// 状态管理
const fundPool = ref({
  initial_amount: 0,
  current_balance: 0,
  total_income: 0,
  total_expenses: 0
})

const showAddModal = ref(false)
const showQuickStats = ref(false)
const trendPeriod = ref('7d')
const showDatePicker = ref(false)
const selectedPeriod = ref('current')
const customMonth = ref('')
const selectedDate = ref(new Date())

const monthlyExpense = ref(0)
const monthlyIncome = ref(0)
const todayExpense = ref(0)
const weeklyExpense = ref(0)
const transactionCount = ref(0)

const expenseTrendData = ref(null)
const categoryData = ref(null)

// 计算属性
const currentMonth = computed(() => {
  if (selectedPeriod.value === 'thisYear') {
    return `${selectedDate.value.getFullYear()}年`
  } else if (selectedPeriod.value === 'thisWeek') {
    const weekStart = getWeekStart(selectedDate.value)
    const weekEnd = new Date(weekStart)
    weekEnd.setDate(weekEnd.getDate() + 6)
    return `${weekStart.getMonth() + 1}月${weekStart.getDate()}日 - ${weekEnd.getMonth() + 1}月${weekEnd.getDate()}日`
  }
  return `${selectedDate.value.getFullYear()}年${selectedDate.value.getMonth() + 1}月`
})

// 获取一周的开始日期（周日）
function getWeekStart(date) {
  const d = new Date(date)
  const day = d.getDay()
  const diff = d.getDate() - day
  return new Date(d.setDate(diff))
}

const monthlyNet = computed(() => {
  return monthlyIncome.value - monthlyExpense.value
})

const savingRate = computed(() => {
  if (monthlyIncome.value === 0) return 0
  return ((monthlyIncome.value - monthlyExpense.value) / monthlyIncome.value) * 100
})

const periodLabel = computed(() => {
  switch (selectedPeriod.value) {
    case 'thisWeek':
      return '本周'
    case 'current':
      return '本月'
    case 'lastMonth':
      return '上月'
    case 'thisYear':
      return '今年'
    case 'custom':
      return '当期'
    default:
      return '本月'
  }
})

const dailyAverage = computed(() => {
  const today = new Date()
  const dayOfMonth = today.getDate()
  return monthlyExpense.value / dayOfMonth
})

const recentTransactions = computed(() => {
  return transactionStore.transactions.slice(0, 5)
})

const hasExpenseData = computed(() => {
  return expenseTrendData.value?.datasets?.[0]?.data?.some(v => v > 0)
})

const hasCategoryData = computed(() => {
  return categoryData.value?.datasets?.[0]?.data?.length > 0
})

// 分类标签
const categoryLabels = {
  food: '餐饮',
  transport: '交通',
  shopping: '购物',
  utilities: '水电',
  entertainment: '娱乐',
  medical: '医疗',
  education: '教育',
  salary: '工资',
  bonus: '奖金',
  other: '其他'
}

// 辅助函数
function getCategoryLabel(category) {
  return categoryLabels[category] || category
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('zh-CN', {
    month: 'numeric',
    day: 'numeric'
  })
}

function getPercentage(value, max) {
  if (max === 0) return 0
  return Math.round((value / max) * 100)
}

// 日期选择函数
function selectPeriod(period) {
  selectedPeriod.value = period
  const now = new Date()

  if (period === 'thisWeek') {
    selectedDate.value = now
  } else if (period === 'current') {
    selectedDate.value = now
  } else if (period === 'lastMonth') {
    const lastMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1)
    selectedDate.value = lastMonth
  } else if (period === 'thisYear') {
    selectedDate.value = new Date(now.getFullYear(), 0, 1)
  }

  showDatePicker.value = false
  loadData()
}

function selectCustomMonth() {
  if (customMonth.value) {
    const [year, month] = customMonth.value.split('-')
    selectedDate.value = new Date(parseInt(year), parseInt(month) - 1, 1)
    selectedPeriod.value = 'custom'
    showDatePicker.value = false
    loadData()
  }
}

// 图表配置
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      padding: 8,
      cornerRadius: 4,
      titleFont: { size: 12 },
      bodyFont: { size: 12 },
      callbacks: {
        label: (context) => `¥${context.parsed.y.toFixed(2)}`
      }
    }
  },
  scales: {
    x: {
      grid: {
        display: false
      },
      ticks: {
        font: { size: 11 },
        color: '#9ca3af'
      }
    },
    y: {
      beginAtZero: true,
      grid: {
        color: '#f3f4f6'
      },
      ticks: {
        font: { size: 11 },
        color: '#9ca3af',
        callback: (value) => `¥${value}`
      }
    }
  }
}

const pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
      labels: {
        padding: 8,
        font: { size: 11 },
        color: '#4b5563'
      }
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      padding: 8,
      cornerRadius: 4,
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

// 数据加载
async function loadFundPool() {
  try {
    console.log('Loading fund pool...')
    const response = await axios.get('/api/fund-pool/')
    console.log('Fund pool API response:', response.data)

    // 确保数字类型正确
    fundPool.value = {
      initial_amount: parseFloat(response.data.initial_amount) || 47830,
      current_balance: parseFloat(response.data.current_balance) || 47830,
      total_income: parseFloat(response.data.total_income) || 0,
      total_expenses: parseFloat(response.data.total_expenses) || 0
    }

    console.log('Fund pool after assignment:', fundPool.value)
  } catch (error) {
    console.error('Failed to load fund pool:', error)
    // 如果失败，设置默认值
    fundPool.value = {
      initial_amount: 47830,
      current_balance: 47830,
      total_income: 0,
      total_expenses: 0
    }
  }
}

async function loadStatistics() {
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const weekStart = new Date(today)
  weekStart.setDate(weekStart.getDate() - weekStart.getDay())

  // 数据已经在 API 层面按时间段过滤，直接统计即可
  let todayExp = 0
  let weekExp = 0
  let monthInc = 0
  let monthExp = 0
  const categoryTotals = {}

  const days = trendPeriod.value === '7d' ? 7 : 30
  const trendData = {}

  // 初始化趋势数据
  for (let i = days - 1; i >= 0; i--) {
    const date = new Date()
    date.setDate(date.getDate() - i)
    const dateStr = `${date.getMonth() + 1}/${date.getDate()}`
    trendData[dateStr] = 0
  }

  transactionStore.transactions.forEach(t => {
    const tDate = new Date(t.date)

    // 今日支出（用于快捷统计）
    if (tDate >= today && t.type === 'expense') {
      todayExp += parseFloat(t.amount)
    }

    // 本周支出（用于快捷统计）
    if (tDate >= weekStart && t.type === 'expense') {
      weekExp += parseFloat(t.amount)
    }

    // 选定时期的收支统计
    if (t.type === 'income') {
      monthInc += parseFloat(t.amount)
    } else {
      monthExp += parseFloat(t.amount)

      if (!categoryTotals[t.category]) {
        categoryTotals[t.category] = 0
      }
      categoryTotals[t.category] += parseFloat(t.amount)
    }

    // 趋势数据（最近7天或30天）
    const daysDiff = Math.floor((now - tDate) / (1000 * 60 * 60 * 24))
    if (daysDiff >= 0 && daysDiff < days && t.type === 'expense') {
      const dateStr = `${tDate.getMonth() + 1}/${tDate.getDate()}`
      if (trendData[dateStr] !== undefined) {
        trendData[dateStr] += parseFloat(t.amount)
      }
    }
  })

  todayExpense.value = todayExp
  weeklyExpense.value = weekExp
  monthlyIncome.value = monthInc
  monthlyExpense.value = monthExp
  transactionCount.value = transactionStore.transactions.length

  // 设置趋势图数据
  expenseTrendData.value = {
    labels: Object.keys(trendData),
    datasets: [{
      label: '支出',
      data: Object.values(trendData),
      borderColor: '#ef4444',
      backgroundColor: 'rgba(239, 68, 68, 0.1)',
      tension: 0.4,
      fill: true,
      pointRadius: 3,
      pointHoverRadius: 5
    }]
  }

  // 设置分类图数据
  const sortedCategories = Object.entries(categoryTotals)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)

  if (sortedCategories.length > 0) {
    categoryData.value = {
      labels: sortedCategories.map(([cat]) => getCategoryLabel(cat)),
      datasets: [{
        data: sortedCategories.map(([_, amount]) => amount),
        backgroundColor: [
          '#3b82f6',
          '#10b981',
          '#f59e0b',
          '#ef4444',
          '#8b5cf6'
        ],
        borderWidth: 0
      }]
    }
  }
}

function handleAddSuccess() {
  showAddModal.value = false
  loadData()
}

async function loadData() {
  await loadFundPool()

  // 根据选择的时间段获取数据
  let startDate, endDate
  if (selectedPeriod.value === 'thisYear') {
    startDate = new Date(selectedDate.value.getFullYear(), 0, 1)
    endDate = new Date(selectedDate.value.getFullYear(), 11, 31, 23, 59, 59)
  } else if (selectedPeriod.value === 'thisWeek') {
    startDate = getWeekStart(selectedDate.value)
    endDate = new Date(startDate)
    endDate.setDate(endDate.getDate() + 6)
    endDate.setHours(23, 59, 59, 999)
  } else {
    startDate = new Date(selectedDate.value.getFullYear(), selectedDate.value.getMonth(), 1)
    endDate = new Date(selectedDate.value.getFullYear(), selectedDate.value.getMonth() + 1, 0, 23, 59, 59)
  }

  // 使用日期范围参数查询数据库
  await transactionStore.fetchTransactions({
    start_date: startDate.toISOString(),
    end_date: endDate.toISOString()
  })

  await loadStatistics()
}

// 监听趋势周期变化
watch(trendPeriod, () => {
  loadStatistics()
})

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}
</style>