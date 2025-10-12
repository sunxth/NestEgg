<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div v-show="!isLoading" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 page-fade-in">
      <!-- 页面标题和日期 -->
      <div class="mb-6">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-semibold text-gray-900 dark:text-white">财务概览</h1>
          <DateRangePicker @change="handleDateRangeChange" />
        </div>
      </div>

      <!-- 资产和流动性区 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- 资金池余额 -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm dark:shadow-gray-700/30 hover:shadow-lg dark:hover:shadow-gray-700/50 hover:-translate-y-1 transition-all duration-300 overflow-hidden">
          <div class="bg-gradient-to-r from-indigo-500 to-indigo-600 px-6 py-4">
            <h3 class="text-white text-sm font-medium mb-2">资金池余额</h3>
            <p class="text-3xl font-semibold text-white leading-tight apple-numbers">
              ¥{{ fundPool?.current_balance?.toFixed(2) || '0.00' }}
            </p>
          </div>
          <div class="px-6 py-4">
            <div class="grid grid-cols-3 gap-4 text-center">
              <div>
                <p class="text-xs text-gray-500 dark:text-gray-400 mb-1.5">初始资金</p>
                <p class="text-lg font-semibold text-gray-900 dark:text-white apple-numbers">¥{{ (fundPool?.initial_amount || 0).toFixed(0) }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500 dark:text-gray-400 mb-1.5">累计收入</p>
                <p class="text-lg font-semibold text-green-600 apple-numbers">+¥{{ (fundPool?.total_income || 0).toFixed(0) }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500 dark:text-gray-400 mb-1.5">累计支出</p>
                <p class="text-lg font-semibold text-red-600 apple-numbers">-¥{{ (fundPool?.total_expenses || 0).toFixed(0) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 收支对比 -->
        <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm dark:shadow-gray-700/30 hover:shadow-lg dark:hover:shadow-gray-700/50 hover:-translate-y-1 transition-all duration-300">
          <h3 class="text-sm font-medium text-gray-900 dark:text-white mb-4">{{ periodLabel }}收支</h3>
          <div class="space-y-4">
            <!-- 收入条 -->
            <div>
              <div class="flex justify-between items-center mb-1">
                <span class="text-sm text-gray-600 dark:text-gray-300">收入</span>
                <span class="text-sm font-semibold text-gray-900 dark:text-white apple-numbers">¥{{ monthlyIncome.toFixed(2) }}</span>
              </div>
              <div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2">
                <div class="bg-green-500 h-2 rounded-full transition-all duration-500"
                     :style="{width: `${getPercentage(monthlyIncome, Math.max(monthlyIncome, monthlyExpense))}%`}"></div>
              </div>
            </div>
            <!-- 支出条 -->
            <div>
              <div class="flex justify-between items-center mb-1">
                <span class="text-sm text-gray-600 dark:text-gray-300">支出</span>
                <span class="text-sm font-semibold text-gray-900 dark:text-white apple-numbers">¥{{ monthlyExpense.toFixed(2) }}</span>
              </div>
              <div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2">
                <div class="bg-red-500 h-2 rounded-full transition-all duration-500"
                     :style="{width: `${getPercentage(monthlyExpense, Math.max(monthlyIncome, monthlyExpense))}%`}"></div>
              </div>
            </div>
            <!-- 结余 -->
            <div class="pt-3 border-t border-gray-100 dark:border-gray-700">
              <div class="flex justify-between items-center">
                <span class="text-sm font-medium text-gray-600 dark:text-gray-300">结余</span>
                <span class="text-lg font-semibold apple-numbers" :class="monthlyNet >= 0 ? 'text-indigo-600' : 'text-red-600'">
                  {{ monthlyNet >= 0 ? '+' : '-' }}¥{{ Math.abs(monthlyNet).toFixed(2) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 核心指标区 - 缩小版 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <!-- 净收入 -->
        <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm dark:shadow-gray-700/30 hover:shadow-md dark:hover:shadow-gray-700/50 transition-all duration-300">
          <div class="mb-1">
            <span class="text-xs text-gray-500 dark:text-gray-400">{{ periodLabel }}净收入</span>
          </div>
          <p class="text-2xl font-bold leading-tight apple-numbers" :class="monthlyNet >= 0 ? 'text-gray-900 dark:text-white' : 'text-red-600'">
            {{ monthlyNet >= 0 ? '+' : '-' }}¥{{ Math.abs(monthlyNet).toFixed(0) }}
          </p>
          <div class="flex items-center gap-3 mt-1.5">
            <span class="text-xs text-gray-500 dark:text-gray-400 apple-numbers">
              收入 ¥{{ monthlyIncome.toFixed(0) }}
            </span>
            <span class="text-xs text-gray-500 dark:text-gray-400 apple-numbers">
              支出 ¥{{ monthlyExpense.toFixed(0) }}
            </span>
          </div>
        </div>

        <!-- 储蓄率 -->
        <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm dark:shadow-gray-700/30 hover:shadow-md dark:hover:shadow-gray-700/50 transition-all duration-300">
          <div class="flex items-start justify-between mb-2">
            <div>
              <span class="text-xs text-gray-500 dark:text-gray-400">储蓄率</span>
              <p class="text-2xl font-bold text-gray-900 dark:text-white mt-1 leading-tight apple-numbers">{{ savingRate.toFixed(0) }}%</p>
            </div>
            <!-- 环形图标 - 缩小版 -->
            <div class="relative w-12 h-12">
              <svg class="transform -rotate-90" width="48" height="48">
                <circle cx="24" cy="24" r="20" fill="none" stroke="#E5E7EB" stroke-width="4"/>
                <circle cx="24" cy="24" r="20" fill="none"
                        :stroke="savingRate >= 30 ? '#10B981' : savingRate >= 10 ? '#F59E0B' : '#EF4444'"
                        stroke-width="4"
                        :stroke-dasharray="`${2 * Math.PI * 20}`"
                        :stroke-dashoffset="`${2 * Math.PI * 20 * (1 - Math.min(savingRate, 100) / 100)}`"
                        class="transition-all duration-500"
                        stroke-linecap="round"/>
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-xs font-bold apple-numbers" :class="savingRate >= 30 ? 'text-green-600' : savingRate >= 10 ? 'text-yellow-600' : 'text-red-600'">
                  {{ savingRate.toFixed(0) }}%
                </span>
              </div>
            </div>
          </div>
          <!-- 进度条 -->
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-1.5">
            <div class="h-2 rounded-full transition-all duration-500"
                 :class="savingRate >= 30 ? 'bg-green-500' : savingRate >= 10 ? 'bg-yellow-500' : 'bg-red-500'"
                 :style="{width: `${Math.min(savingRate, 100)}%`}"></div>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-xs font-medium"
                  :class="savingRate >= 30 ? 'text-green-600' : savingRate >= 10 ? 'text-yellow-600' : 'text-red-600'">
              {{ savingRate >= 30 ? '✨ 优秀' : savingRate >= 10 ? '👍 良好' : '⚠️ 需要改善' }}
            </span>
            <span class="text-xs text-gray-500 dark:text-gray-400">
              目标: 30%
            </span>
          </div>
        </div>
      </div>

      <!-- 趋势和分析区 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- 支出趋势 -->
        <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm dark:shadow-gray-700/30 hover:shadow-lg dark:hover:shadow-gray-700/50 hover:-translate-y-1 transition-all duration-300">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-sm font-medium text-gray-900 dark:text-white">支出趋势</h3>
            <div class="flex gap-1">
              <button @click="trendPeriod = '7d'"
                      :class="trendPeriod === '7d' ? 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white' : 'text-gray-500 dark:text-gray-400'"
                      class="px-2 py-1 text-xs rounded transition-colors">
                7天
              </button>
              <button @click="trendPeriod = '30d'"
                      :class="trendPeriod === '30d' ? 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white' : 'text-gray-500 dark:text-gray-400'"
                      class="px-2 py-1 text-xs rounded transition-colors">
                30天
              </button>
            </div>
          </div>
          <div class="h-48">
            <Line v-if="expenseTrendData && hasExpenseData" :data="expenseTrendData" :options="chartOptions" />
            <div v-else class="h-full flex items-center justify-center text-gray-400 dark:text-gray-500">
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
        <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm dark:shadow-gray-700/30 hover:shadow-lg dark:hover:shadow-gray-700/50 hover:-translate-y-1 transition-all duration-300">
          <h3 class="text-sm font-medium text-gray-900 dark:text-white mb-4">支出分类</h3>
          <div class="h-48">
            <Doughnut v-if="categoryData && hasCategoryData" :data="categoryData" :options="pieOptions" />
            <div v-else class="h-full flex items-center justify-center text-gray-400 dark:text-gray-500">
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
                class="flex items-center gap-2 mb-4 text-sm text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors">
          <svg class="w-4 h-4 transition-transform" :class="showQuickStats ? 'rotate-90' : ''"
               fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
          快捷统计
        </button>

        <div v-show="showQuickStats" class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm dark:shadow-gray-700/30 hover:shadow-md dark:hover:shadow-gray-700/50 hover:-translate-y-0.5 transition-all duration-200 cursor-pointer">
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-1.5">今日支出</p>
            <p class="text-xl font-semibold text-gray-900 dark:text-white leading-tight apple-numbers">¥{{ todayExpense.toFixed(0) }}</p>
          </div>
          <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm dark:shadow-gray-700/30 hover:shadow-md dark:hover:shadow-gray-700/50 hover:-translate-y-0.5 transition-all duration-200 cursor-pointer">
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-1.5">本周支出</p>
            <p class="text-xl font-semibold text-gray-900 dark:text-white leading-tight apple-numbers">¥{{ weeklyExpense.toFixed(0) }}</p>
          </div>
          <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm dark:shadow-gray-700/30 hover:shadow-md dark:hover:shadow-gray-700/50 hover:-translate-y-0.5 transition-all duration-200 cursor-pointer">
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-1.5">交易笔数</p>
            <p class="text-xl font-semibold text-gray-900 dark:text-white leading-tight apple-numbers">{{ transactionCount }}</p>
          </div>
          <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm dark:shadow-gray-700/30 hover:shadow-md dark:hover:shadow-gray-700/50 hover:-translate-y-0.5 transition-all duration-200 cursor-pointer">
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-1.5">日均支出</p>
            <p class="text-xl font-semibold text-gray-900 dark:text-white leading-tight apple-numbers">¥{{ dailyAverage.toFixed(0) }}</p>
          </div>
        </div>
      </div>

      <!-- 最近交易 -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm dark:shadow-gray-700/30 hover:shadow-lg dark:hover:shadow-gray-700/50 hover:-translate-y-1 transition-all duration-300">
        <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center">
          <div class="flex items-center gap-3">
            <h3 class="text-sm font-medium text-gray-900 dark:text-white">最近交易</h3>
            <!-- 显示条数选择器 -->
            <div class="relative" ref="limitDropdownRef">
              <button
                @click.stop="showLimitDropdown = !showLimitDropdown"
                class="inline-flex items-center gap-1 px-2 py-1 text-xs text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded transition-colors"
              >
                <span>显示: {{ recentLimit }}条</span>
                <svg class="w-3 h-3 transition-transform" :class="showLimitDropdown ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>

              <!-- 下拉菜单 -->
              <Transition
                enter-active-class="transition duration-100 ease-out"
                enter-from-class="opacity-0 scale-95"
                enter-to-class="opacity-100 scale-100"
                leave-active-class="transition duration-75 ease-in"
                leave-from-class="opacity-100 scale-100"
                leave-to-class="opacity-0 scale-95"
              >
                <div
                  v-if="showLimitDropdown"
                  class="absolute left-0 top-full mt-1 w-24 bg-white dark:bg-gray-700 rounded-lg shadow-lg border border-gray-200 dark:border-gray-600 py-1 z-10"
                >
                  <button
                    v-for="option in [5, 10, 15, 20]"
                    :key="option"
                    @click.stop="setRecentLimit(option)"
                    class="w-full px-3 py-1.5 text-xs text-left hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                    :class="recentLimit === option ? 'text-indigo-600 dark:text-indigo-400 font-medium' : 'text-gray-700 dark:text-gray-300'"
                  >
                    {{ option }}条
                  </button>
                </div>
              </Transition>
            </div>
          </div>
          <router-link to="/transactions" class="text-xs text-indigo-600 hover:text-indigo-700 transition-colors">
            查看全部 →
          </router-link>
        </div>
        <div class="divide-y divide-gray-100 dark:divide-gray-700">
          <div v-for="transaction in recentTransactions" :key="transaction.id"
               class="px-6 py-3 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
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
                  <p class="text-sm text-gray-900 dark:text-white">{{ transaction.description || getCategoryLabel(transaction.category) }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(transaction.date) }} · {{ getCategoryLabel(transaction.category) }}</p>
                </div>
              </div>
              <p class="text-sm font-medium apple-numbers"
                 :class="transaction.type === 'income' ? 'text-green-600' : 'text-red-600'">
                {{ transaction.type === 'income' ? '+' : '-' }}¥{{ parseFloat(transaction.amount).toFixed(2) }}
              </p>
            </div>
          </div>
          <div v-if="recentTransactions.length === 0" class="px-6 py-12 text-center text-gray-400 dark:text-gray-500">
            <p class="text-sm">暂无交易记录</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 悬浮快速记账按钮 (FAB) -->
    <button v-if="authStore.isAdmin"
            @click="showAddModal = true"
            class="fixed bottom-6 right-6 w-14 h-14 bg-indigo-600 text-white rounded-full shadow-lg hover:bg-indigo-700 hover:shadow-xl hover:scale-110 transition-all duration-200 flex items-center justify-center group z-40">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
      </svg>
      <span class="absolute right-16 bg-gray-900 dark:bg-gray-700 text-white px-2 py-1 rounded text-xs whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
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
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
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
import DateRangePicker from '@/components/DateRangePicker.vue'
import axios from '@/utils/axios'

// 点击外部关闭下拉菜单
function handleClickOutside(event) {
  if (limitDropdownRef.value && !limitDropdownRef.value.contains(event.target)) {
    showLimitDropdown.value = false
  }
}

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
const dateRange = ref({ start: null, end: null })
const isLoading = ref(true)  // 初始为 true，避免数据闪烁
const showLimitDropdown = ref(false)
const recentLimit = ref(parseInt(localStorage.getItem('dashboard_recent_limit')) || 5)
const limitDropdownRef = ref(null)

const monthlyExpense = ref(0)
const monthlyIncome = ref(0)
const todayExpense = ref(0)
const weeklyExpense = ref(0)
const transactionCount = ref(0)

// 防抖定时器
let loadDataDebounceTimer = null

const expenseTrendData = ref(null)
const categoryData = ref(null)

// 计算属性
const monthlyNet = computed(() => {
  return monthlyIncome.value - monthlyExpense.value
})

const savingRate = computed(() => {
  if (monthlyIncome.value === 0) return 0
  return ((monthlyIncome.value - monthlyExpense.value) / monthlyIncome.value) * 100
})

const periodLabel = computed(() => {
  return '当期'
})

const dailyAverage = computed(() => {
  const today = new Date()
  const dayOfMonth = today.getDate()
  return monthlyExpense.value / dayOfMonth
})

const recentTransactions = computed(() => {
  return transactionStore.transactions.slice(0, recentLimit.value)
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

// 日期范围变化处理（带防抖）
function handleDateRangeChange(range) {
  dateRange.value = range

  // 清除之前的定时器
  if (loadDataDebounceTimer) {
    clearTimeout(loadDataDebounceTimer)
  }

  // 300ms 防抖
  loadDataDebounceTimer = setTimeout(() => {
    loadData()
  }, 300)
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

function setRecentLimit(limit) {
  recentLimit.value = limit
  localStorage.setItem('dashboard_recent_limit', limit)
  showLimitDropdown.value = false
}

async function loadData() {
  isLoading.value = true

  try {
    await loadFundPool()

    // 如果还没有选择日期范围，使用本月
    if (!dateRange.value.start || !dateRange.value.end) {
      const now = new Date()
      dateRange.value = {
        start: new Date(now.getFullYear(), now.getMonth(), 1),
        end: new Date(now.getFullYear(), now.getMonth() + 1, 0)
      }
    }

    const startDate = new Date(dateRange.value.start)
    startDate.setHours(0, 0, 0, 0)

    const endDate = new Date(dateRange.value.end)
    endDate.setHours(23, 59, 59, 999)

    // 使用日期范围参数查询数据库
    await transactionStore.fetchTransactions({
      start_date: startDate.toISOString(),
      end_date: endDate.toISOString()
    })

    await loadStatistics()
  } finally {
    // 延迟关闭 loading，确保所有 DOM 更新完成，避免闪烁
    setTimeout(() => {
      isLoading.value = false
    }, 150)
  }
}

// 监听趋势周期变化
watch(trendPeriod, () => {
  loadStatistics()
})

onMounted(() => {
  // 不需要在这里调用 loadData()，DateRangePicker 初始化时会自动触发 change 事件
  // 这样避免重复加载数据
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

/* 整页淡入动画 - 更慢更优雅 */
.page-fade-in {
  animation: pageFadeIn 0.8s ease-out;
}

@keyframes pageFadeIn {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 专业数字字体 - Inter */
:deep(.apple-numbers) {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.015em;
  font-feature-settings: 'tnum' 1, 'cv05' 1, 'cv11' 1;
  font-weight: 600;
}
</style>