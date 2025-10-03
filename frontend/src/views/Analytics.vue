<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">数据统计</h1>

      <!-- 年度选择器 - 现代化设计 -->
      <div class="relative inline-block">
        <button @click="showYearPicker = !showYearPicker"
                class="inline-flex items-center gap-2 px-4 py-2.5 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm dark:shadow-gray-700/30 hover:shadow-md hover:border-indigo-300 dark:hover:border-indigo-600 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900">
          <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          <span class="font-semibold text-gray-700 dark:text-gray-300">{{ selectedYear }}年</span>
          <svg class="w-4 h-4 text-gray-500 dark:text-gray-400 transition-transform duration-200"
               :class="{'rotate-180': showYearPicker}"
               fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </button>

        <!-- 下拉菜单 -->
        <div v-show="showYearPicker"
             class="absolute right-0 mt-2 w-40 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-xl dark:shadow-gray-700/30 z-50 overflow-hidden max-h-64 overflow-y-auto">
          <div class="py-1">
            <button v-for="year in availableYears" :key="year"
                    @click="selectYear(year)"
                    class="w-full px-4 py-2.5 text-left hover:bg-indigo-50 dark:hover:bg-indigo-900/30 transition-colors duration-150 flex items-center justify-between group"
                    :class="selectedYear === year ? 'bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-400 font-semibold' : 'text-gray-700 dark:text-gray-300'">
              <span>{{ year }}年</span>
              <svg v-if="selectedYear === year" class="w-5 h-5 text-indigo-600 dark:text-indigo-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 年度概览 -->
    <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
      <!-- 年度总收入 -->
      <div class="relative overflow-hidden rounded-lg shadow-lg bg-gradient-to-br from-green-50 to-emerald-100 p-5">
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <dt class="text-sm font-medium text-green-700 mb-1">年度总收入</dt>
            <dd class="text-2xl font-bold text-green-600 mb-2">
              ¥{{ yearSummary.totalIncome.toFixed(2) }}
            </dd>
            <p class="text-xs text-green-600">月均 ¥{{ (yearSummary.totalIncome / 12).toFixed(2) }}</p>
          </div>
          <div class="flex-shrink-0">
            <div class="w-12 h-12 bg-green-500 bg-opacity-20 rounded-full flex items-center justify-center">
              <svg class="w-7 h-7 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- 年度总支出 -->
      <div class="relative overflow-hidden rounded-lg shadow-lg bg-gradient-to-br from-red-50 to-rose-100 p-5">
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <dt class="text-sm font-medium text-red-700 mb-1">年度总支出</dt>
            <dd class="text-2xl font-bold text-red-600 mb-2">
              ¥{{ yearSummary.totalExpense.toFixed(2) }}
            </dd>
            <p class="text-xs text-red-600">月均 ¥{{ (yearSummary.totalExpense / 12).toFixed(2) }}</p>
          </div>
          <div class="flex-shrink-0">
            <div class="w-12 h-12 bg-red-500 bg-opacity-20 rounded-full flex items-center justify-center">
              <svg class="w-7 h-7 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- 年度结余 -->
      <div class="relative overflow-hidden rounded-lg shadow-lg bg-gradient-to-br from-blue-50 to-indigo-100 p-5">
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <dt class="text-sm font-medium text-blue-700 mb-1">年度结余</dt>
            <dd class="text-2xl font-bold mb-2"
                :class="yearSummary.netAmount >= 0 ? 'text-blue-600' : 'text-red-600'">
              {{ yearSummary.netAmount >= 0 ? '+' : '' }}¥{{ yearSummary.netAmount.toFixed(2) }}
            </dd>
            <p class="text-xs text-blue-600">储蓄率 {{ yearSummary.savingRate.toFixed(1) }}%</p>
          </div>
          <div class="flex-shrink-0">
            <div class="w-12 h-12 bg-blue-500 bg-opacity-20 rounded-full flex items-center justify-center">
              <svg class="w-7 h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- 最大支出月 -->
      <div class="relative overflow-hidden rounded-lg shadow-lg bg-gradient-to-br from-orange-50 to-amber-100 p-5">
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <dt class="text-sm font-medium text-orange-700 mb-1">最大支出月</dt>
            <dd class="text-2xl font-bold text-orange-600 mb-2">
              {{ yearSummary.maxExpenseMonth }}月
            </dd>
            <p class="text-xs text-orange-600">¥{{ yearSummary.maxExpenseAmount.toFixed(2) }}</p>
          </div>
          <div class="flex-shrink-0">
            <div class="w-12 h-12 bg-orange-500 bg-opacity-20 rounded-full flex items-center justify-center">
              <svg class="w-7 h-7 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- 最少支出月 -->
      <div class="relative overflow-hidden rounded-lg shadow-lg bg-gradient-to-br from-purple-50 to-violet-100 p-5">
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <dt class="text-sm font-medium text-purple-700 mb-1">最少支出月</dt>
            <dd class="text-2xl font-bold text-purple-600 mb-2">
              {{ yearSummary.minExpenseMonth }}月
            </dd>
            <p class="text-xs text-purple-600">¥{{ yearSummary.minExpenseAmount.toFixed(2) }}</p>
          </div>
          <div class="flex-shrink-0">
            <div class="w-12 h-12 bg-purple-500 bg-opacity-20 rounded-full flex items-center justify-center">
              <svg class="w-7 h-7 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 月度趋势图 -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow dark:shadow-gray-700/30">
        <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">月度收支趋势</h2>
        <div class="h-64">
          <Line v-if="trendChartData" :data="trendChartData" :options="lineChartOptions" />
        </div>
      </div>

      <!-- 分类支出饼图 -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow dark:shadow-gray-700/30">
        <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">支出分类占比</h2>
        <div class="h-64">
          <Doughnut v-if="categoryChartData" :data="categoryChartData" :options="doughnutChartOptions" />
        </div>
      </div>

      <!-- 月度对比柱状图 -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow dark:shadow-gray-700/30">
        <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">月度收支对比</h2>
        <div class="h-64">
          <Bar v-if="monthlyChartData" :data="monthlyChartData" :options="barChartOptions" />
        </div>
      </div>

      <!-- 分类趋势图 -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow dark:shadow-gray-700/30">
        <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">分类支出趋势</h2>
        <div class="h-64">
          <Line v-if="categoryTrendData" :data="categoryTrendData" :options="categoryLineOptions" />
        </div>
      </div>
    </div>

    <!-- 分类支出排行 -->
    <div class="mt-6 bg-white dark:bg-gray-800 p-6 rounded-lg shadow dark:shadow-gray-700/30">
      <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4">支出分类排行</h2>
      <div class="space-y-3">
        <div v-for="(item, index) in categoryRanking" :key="item.category"
             class="flex items-center justify-between">
          <div class="flex items-center gap-3 flex-1">
            <span class="w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center text-sm font-medium text-gray-900 dark:text-white">
              {{ index + 1 }}
            </span>
            <span class="font-medium text-gray-900 dark:text-white">{{ getCategoryLabel(item.category) }}</span>
            <div class="flex-1 mx-4">
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div class="bg-indigo-600 h-2 rounded-full" :style="{width: `${item.percentage}%`}"></div>
              </div>
            </div>
          </div>
          <div class="text-right">
            <p class="font-semibold text-gray-900 dark:text-white">¥{{ item.total.toFixed(2) }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">{{ item.percentage.toFixed(1) }}% · {{ item.count }}笔</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Line, Bar, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { useTransactionStore } from '@/stores/transaction'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const transactionStore = useTransactionStore()

// 动态生成年份列表：从 2024 年开始到当前年份后 2 年
const currentYear = new Date().getFullYear()
const startYear = 2024 // NestEgg 项目启动年份
const availableYears = computed(() => {
  const years = []
  for (let year = startYear; year <= currentYear + 2; year++) {
    years.push(year)
  }
  return years
})

const selectedYear = ref(currentYear)
const showYearPicker = ref(false)

const trendChartData = ref(null)
const categoryChartData = ref(null)
const monthlyChartData = ref(null)
const categoryTrendData = ref(null)

const yearSummary = ref({
  totalIncome: 0,
  totalExpense: 0,
  netAmount: 0,
  savingRate: 0,
  maxExpenseMonth: 0,
  maxExpenseAmount: 0,
  minExpenseMonth: 0,
  minExpenseAmount: 999999
})

const categoryRanking = ref([])

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

const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
    tooltip: {
      callbacks: {
        label: (context) => `${context.dataset.label}: ¥${context.parsed.y.toFixed(2)}`
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

const barChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
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

const doughnutChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
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

const categoryLineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      stacked: true,
      ticks: {
        callback: (value) => `¥${value}`
      }
    }
  }
}

function getCategoryLabel(category) {
  return categoryLabels[category] || category
}

function selectYear(year) {
  selectedYear.value = year
  showYearPicker.value = false
  loadData()
}

async function loadData() {
  // 获取全年数据
  const startDate = new Date(selectedYear.value, 0, 1)
  const endDate = new Date(selectedYear.value, 11, 31)

  await transactionStore.fetchTransactions({
    start_date: startDate,
    end_date: endDate
  })

  // 初始化月度数据
  const monthlyData = {}
  for (let i = 1; i <= 12; i++) {
    monthlyData[i] = {
      income: 0,
      expense: 0,
      categories: {}
    }
  }

  // 分析交易数据
  let totalIncome = 0
  let totalExpense = 0
  const categoryTotals = {}

  transactionStore.transactions.forEach(t => {
    const date = new Date(t.date)
    const month = date.getMonth() + 1

    if (date.getFullYear() === selectedYear.value) {
      if (t.type === 'income') {
        monthlyData[month].income += parseFloat(t.amount)
        totalIncome += parseFloat(t.amount)
      } else {
        monthlyData[month].expense += parseFloat(t.amount)
        totalExpense += parseFloat(t.amount)

        // 分类统计
        if (!categoryTotals[t.category]) {
          categoryTotals[t.category] = { total: 0, count: 0 }
        }
        categoryTotals[t.category].total += parseFloat(t.amount)
        categoryTotals[t.category].count++

        // 月度分类统计
        if (!monthlyData[month].categories[t.category]) {
          monthlyData[month].categories[t.category] = 0
        }
        monthlyData[month].categories[t.category] += parseFloat(t.amount)
      }
    }
  })

  // 计算年度统计
  let maxExpenseMonth = 1
  let maxExpenseAmount = 0
  let minExpenseMonth = 1
  let minExpenseAmount = 999999

  Object.keys(monthlyData).forEach(month => {
    if (monthlyData[month].expense > maxExpenseAmount) {
      maxExpenseAmount = monthlyData[month].expense
      maxExpenseMonth = month
    }
    if (monthlyData[month].expense < minExpenseAmount && monthlyData[month].expense > 0) {
      minExpenseAmount = monthlyData[month].expense
      minExpenseMonth = month
    }
  })

  yearSummary.value = {
    totalIncome,
    totalExpense,
    netAmount: totalIncome - totalExpense,
    savingRate: totalIncome > 0 ? ((totalIncome - totalExpense) / totalIncome * 100) : 0,
    maxExpenseMonth,
    maxExpenseAmount,
    minExpenseMonth,
    minExpenseAmount: minExpenseAmount === 999999 ? 0 : minExpenseAmount
  }

  // 准备图表数据
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']

  // 趋势图数据
  trendChartData.value = {
    labels: months,
    datasets: [
      {
        label: '收入',
        data: months.map((_, i) => monthlyData[i + 1].income),
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        tension: 0.3,
        fill: true
      },
      {
        label: '支出',
        data: months.map((_, i) => monthlyData[i + 1].expense),
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        tension: 0.3,
        fill: true
      },
      {
        label: '结余',
        data: months.map((_, i) => monthlyData[i + 1].income - monthlyData[i + 1].expense),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.3,
        fill: true
      }
    ]
  }

  // 月度对比柱状图
  monthlyChartData.value = {
    labels: months,
    datasets: [
      {
        label: '收入',
        data: months.map((_, i) => monthlyData[i + 1].income),
        backgroundColor: 'rgba(34, 197, 94, 0.8)'
      },
      {
        label: '支出',
        data: months.map((_, i) => monthlyData[i + 1].expense),
        backgroundColor: 'rgba(239, 68, 68, 0.8)'
      }
    ]
  }

  // 分类饼图数据
  const sortedCategories = Object.entries(categoryTotals)
    .sort((a, b) => b[1].total - a[1].total)
    .slice(0, 8)

  categoryChartData.value = {
    labels: sortedCategories.map(([cat]) => getCategoryLabel(cat)),
    datasets: [{
      data: sortedCategories.map(([_, data]) => data.total),
      backgroundColor: [
        '#ef4444',
        '#f97316',
        '#f59e0b',
        '#84cc16',
        '#22c55e',
        '#14b8a6',
        '#06b6d4',
        '#3b82f6'
      ]
    }]
  }

  // 分类排行
  categoryRanking.value = sortedCategories.map(([category, data]) => ({
    category,
    total: data.total,
    count: data.count,
    percentage: (data.total / totalExpense * 100)
  }))

  // 分类趋势图
  const topCategories = sortedCategories.slice(0, 5).map(([cat]) => cat)
  categoryTrendData.value = {
    labels: months,
    datasets: topCategories.map((cat, index) => ({
      label: getCategoryLabel(cat),
      data: months.map((_, i) => monthlyData[i + 1].categories[cat] || 0),
      borderColor: [
        '#ef4444',
        '#f97316',
        '#f59e0b',
        '#84cc16',
        '#22c55e'
      ][index],
      tension: 0.3
    }))
  }
}

// 点击外部关闭下拉菜单
function handleClickOutside(event) {
  const yearPicker = event.target.closest('.relative.inline-block')
  if (!yearPicker) {
    showYearPicker.value = false
  }
}

onMounted(() => {
  loadData()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>