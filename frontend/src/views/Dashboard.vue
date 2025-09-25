<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- 月度预算和资金池 -->
    <div class="mb-8">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-2xl font-bold text-gray-900">{{ currentMonth }} 财务概览</h2>
        <button v-if="authStore.isAdmin" @click="showBudgetModal = true"
                class="text-sm text-indigo-600 hover:text-indigo-900">
          设置预算
        </button>
      </div>

      <!-- 预算进度环和资金池 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 预算进度环 -->
        <div class="bg-white p-6 rounded-lg shadow">
          <div class="text-center">
            <h3 class="text-lg font-medium text-gray-900 mb-4">月度预算</h3>
            <div class="relative inline-block">
              <svg class="transform -rotate-90 w-32 h-32">
                <circle cx="64" cy="64" r="56" stroke="#e5e7eb" stroke-width="12" fill="none" />
                <circle cx="64" cy="64" r="56"
                        :stroke="budgetPercentage > 80 ? '#ef4444' : budgetPercentage > 60 ? '#f59e0b' : '#10b981'"
                        stroke-width="12" fill="none"
                        :stroke-dasharray="`${2 * Math.PI * 56}`"
                        :stroke-dashoffset="`${2 * Math.PI * 56 * (1 - budgetPercentage / 100)}`"
                        stroke-linecap="round" />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <div>
                  <p class="text-3xl font-bold"
                     :class="budgetPercentage > 80 ? 'text-red-600' : budgetPercentage > 60 ? 'text-yellow-600' : 'text-green-600'">
                    {{ budgetPercentage }}%
                  </p>
                  <p class="text-xs text-gray-500">已使用</p>
                </div>
              </div>
            </div>
            <div class="mt-4 space-y-1">
              <p class="text-sm text-gray-600">
                预算：¥{{ monthlyBudget.toFixed(2) }}
              </p>
              <p class="text-sm" :class="budgetRemaining >= 0 ? 'text-green-600' : 'text-red-600'">
                剩余：¥{{ Math.abs(budgetRemaining).toFixed(2) }}
                <span v-if="budgetRemaining < 0" class="text-xs">（超支）</span>
              </p>
            </div>
          </div>
        </div>

        <!-- 资金池余额卡片 -->
        <div class="bg-gradient-to-r from-blue-500 to-blue-600 p-6 rounded-lg shadow text-white">
          <div class="flex justify-between items-start">
            <div>
              <dt class="text-sm font-medium text-blue-100">资金池余额</dt>
              <dd class="mt-2 text-4xl font-bold">
                ¥{{ fundPool?.current_balance?.toFixed(2) || '0.00' }}
              </dd>
              <div class="mt-4 space-y-1">
                <p class="text-xs text-blue-100">初始资金：¥{{ fundPool?.initial_amount?.toFixed(2) || '0.00' }}</p>
                <p class="text-xs text-blue-100">累计收入：¥{{ fundPool?.total_income?.toFixed(2) || '0.00' }}</p>
                <p class="text-xs text-blue-100">累计支出：¥{{ fundPool?.total_expenses?.toFixed(2) || '0.00' }}</p>
              </div>
            </div>
            <svg class="w-12 h-12 text-blue-300" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
          </div>
        </div>

        <!-- 月度收支卡片 -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-medium text-gray-900 mb-4">本月收支</h3>
          <div class="space-y-4">
            <div class="flex justify-between items-center">
              <div class="flex items-center">
                <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </div>
                <span class="ml-3 text-sm font-medium text-gray-900">收入</span>
              </div>
              <span class="text-lg font-semibold text-green-600">¥{{ monthlyIncome.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between items-center">
              <div class="flex items-center">
                <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                  </svg>
                </div>
                <span class="ml-3 text-sm font-medium text-gray-900">支出</span>
              </div>
              <span class="text-lg font-semibold text-red-600">¥{{ monthlyExpense.toFixed(2) }}</span>
            </div>
            <div class="pt-4 border-t border-gray-200">
              <div class="flex justify-between items-center">
                <span class="text-sm font-medium text-gray-900">净收入</span>
                <span class="text-lg font-bold" :class="monthlyNet >= 0 ? 'text-blue-600' : 'text-red-600'">
                  {{ monthlyNet >= 0 ? '+' : '' }}¥{{ Math.abs(monthlyNet).toFixed(2) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-white p-4 rounded-lg shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500">今日支出</p>
            <p class="text-2xl font-semibold text-gray-900">¥{{ todayExpense.toFixed(2) }}</p>
          </div>
          <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
        </div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500">本周支出</p>
            <p class="text-2xl font-semibold text-gray-900">¥{{ weeklyExpense.toFixed(2) }}</p>
          </div>
          <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500">交易笔数</p>
            <p class="text-2xl font-semibold text-gray-900">{{ transactionCount }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
            </svg>
          </div>
        </div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500">储蓄率</p>
            <p class="text-2xl font-semibold text-gray-900">{{ savingRate.toFixed(1) }}%</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 图表和最近交易 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <!-- 支出趋势图 -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-medium text-gray-900 mb-4">7日支出趋势</h3>
        <div class="h-64">
          <Line v-if="expenseTrendData" :data="expenseTrendData" :options="chartOptions" />
        </div>
      </div>

      <!-- 分类支出饼图 -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-medium text-gray-900 mb-4">本月支出分类</h3>
        <div class="h-64">
          <Doughnut v-if="categoryData" :data="categoryData" :options="pieOptions" />
        </div>
      </div>
    </div>

    <!-- 最近交易 -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
        <h2 class="text-lg font-medium text-gray-900">最近交易</h2>
        <div class="flex gap-2">
          <button
            v-if="authStore.isAdmin"
            @click="showAddModal = true"
            class="text-sm text-indigo-600 hover:text-indigo-900"
          >
            快速记账
          </button>
          <router-link to="/transactions" class="text-sm text-indigo-600 hover:text-indigo-900">
            查看全部
          </router-link>
        </div>
      </div>
      <ul class="divide-y divide-gray-200">
        <li v-for="transaction in recentTransactions" :key="transaction.id"
            class="px-6 py-4 hover:bg-gray-50">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-900">{{ transaction.description || getCategoryLabel(transaction.category) }}</p>
              <p class="text-sm text-gray-500">{{ formatDate(transaction.date) }}</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-medium"
                 :class="transaction.type === 'income' ? 'text-green-600' : 'text-red-600'">
                {{ transaction.type === 'income' ? '+' : '-' }}¥{{ transaction.amount.toFixed(2) }}
              </p>
              <p class="text-xs text-gray-500">{{ getCategoryLabel(transaction.category) }}</p>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <AddTransactionModal
      v-if="showAddModal"
      @close="showAddModal = false"
      @success="handleAddSuccess"
    />

    <!-- 预算设置模态框 -->
    <div v-if="showBudgetModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-sm w-full">
        <h3 class="text-lg font-medium text-gray-900 mb-4">设置月度预算</h3>
        <input
          v-model.number="tempBudget"
          type="number"
          min="0"
          step="100"
          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          placeholder="请输入预算金额"
        />
        <div class="mt-4 flex justify-end gap-2">
          <button
            @click="showBudgetModal = false"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            取消
          </button>
          <button
            @click="saveBudget"
            class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700"
          >
            保存
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
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
import axios from 'axios'

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

const fundPool = ref({
  initial_amount: 0,
  current_balance: 0,
  total_income: 0,
  total_expenses: 0
})

const showAddModal = ref(false)
const showBudgetModal = ref(false)
const monthlyBudget = ref(10000) // 默认预算
const tempBudget = ref(10000)
const monthlyExpense = ref(0)
const monthlyIncome = ref(0)
const todayExpense = ref(0)
const weeklyExpense = ref(0)
const transactionCount = ref(0)

const expenseTrendData = ref(null)
const categoryData = ref(null)

const currentMonth = computed(() => {
  const date = new Date()
  return `${date.getFullYear()}年${date.getMonth() + 1}月`
})

const budgetPercentage = computed(() => {
  if (monthlyBudget.value === 0) return 0
  return Math.min(100, Math.round((monthlyExpense.value / monthlyBudget.value) * 100))
})

const budgetRemaining = computed(() => {
  return monthlyBudget.value - monthlyExpense.value
})

const monthlyNet = computed(() => {
  return monthlyIncome.value - monthlyExpense.value
})

const savingRate = computed(() => {
  if (monthlyIncome.value === 0) return 0
  return ((monthlyIncome.value - monthlyExpense.value) / monthlyIncome.value) * 100
})

const recentTransactions = computed(() => {
  return transactionStore.transactions.slice(0, 5)
})

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

function getCategoryLabel(category) {
  return categoryLabels[category] || category
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('zh-CN')
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: (context) => `¥${context.parsed.y.toFixed(2)}`
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
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
        padding: 10,
        font: {
          size: 11
        }
      }
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

async function loadFundPool() {
  try {
    const response = await axios.get('/api/fund-pool')
    fundPool.value = response.data
  } catch (error) {
    console.error('Failed to load fund pool:', error)
  }
}

async function loadStatistics() {
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const weekStart = new Date(today)
  weekStart.setDate(weekStart.getDate() - weekStart.getDay())
  const monthStart = new Date(now.getFullYear(), now.getMonth(), 1)

  // 计算今日、本周、本月数据
  let todayExp = 0
  let weekExp = 0
  let monthInc = 0
  let monthExp = 0
  const categoryTotals = {}
  const last7Days = {}

  // 初始化过去7天的数据
  for (let i = 6; i >= 0; i--) {
    const date = new Date()
    date.setDate(date.getDate() - i)
    const dateStr = date.toLocaleDateString('zh-CN', { month: 'numeric', day: 'numeric' })
    last7Days[dateStr] = 0
  }

  transactionStore.transactions.forEach(t => {
    const tDate = new Date(t.date)

    // 今日支出
    if (tDate >= today && t.type === 'expense') {
      todayExp += parseFloat(t.amount)
    }

    // 本周支出
    if (tDate >= weekStart && t.type === 'expense') {
      weekExp += parseFloat(t.amount)
    }

    // 本月收支
    if (tDate >= monthStart) {
      if (t.type === 'income') {
        monthInc += parseFloat(t.amount)
      } else {
        monthExp += parseFloat(t.amount)

        // 分类统计
        if (!categoryTotals[t.category]) {
          categoryTotals[t.category] = 0
        }
        categoryTotals[t.category] += parseFloat(t.amount)
      }
    }

    // 过去7天趋势
    const daysDiff = Math.floor((now - tDate) / (1000 * 60 * 60 * 24))
    if (daysDiff >= 0 && daysDiff < 7 && t.type === 'expense') {
      const dateStr = tDate.toLocaleDateString('zh-CN', { month: 'numeric', day: 'numeric' })
      if (last7Days[dateStr] !== undefined) {
        last7Days[dateStr] += parseFloat(t.amount)
      }
    }
  })

  todayExpense.value = todayExp
  weeklyExpense.value = weekExp
  monthlyIncome.value = monthInc
  monthlyExpense.value = monthExp
  transactionCount.value = transactionStore.transactions.filter(t => {
    const tDate = new Date(t.date)
    return tDate >= monthStart
  }).length

  // 准备7日趋势图数据
  expenseTrendData.value = {
    labels: Object.keys(last7Days),
    datasets: [{
      label: '支出',
      data: Object.values(last7Days),
      borderColor: 'rgb(239, 68, 68)',
      backgroundColor: 'rgba(239, 68, 68, 0.1)',
      tension: 0.3,
      fill: true
    }]
  }

  // 准备分类饼图数据
  const sortedCategories = Object.entries(categoryTotals)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 6)

  categoryData.value = {
    labels: sortedCategories.map(([cat]) => getCategoryLabel(cat)),
    datasets: [{
      data: sortedCategories.map(([_, amount]) => amount),
      backgroundColor: [
        '#ef4444',
        '#f97316',
        '#f59e0b',
        '#84cc16',
        '#14b8a6',
        '#3b82f6'
      ]
    }]
  }
}

function saveBudget() {
  monthlyBudget.value = tempBudget.value
  showBudgetModal.value = false
  // 这里可以保存到后端或localStorage
  localStorage.setItem('monthlyBudget', monthlyBudget.value.toString())
}

function handleAddSuccess() {
  showAddModal.value = false
  loadData()
}

async function loadData() {
  await loadFundPool()
  await transactionStore.fetchTransactions()
  await loadStatistics()
}

onMounted(() => {
  // 加载保存的预算
  const savedBudget = localStorage.getItem('monthlyBudget')
  if (savedBudget) {
    monthlyBudget.value = parseFloat(savedBudget)
    tempBudget.value = parseFloat(savedBudget)
  }

  loadData()
})
</script>