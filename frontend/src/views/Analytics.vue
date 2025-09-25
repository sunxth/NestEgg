<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">数据统计</h1>
      <select v-model="selectedYear" @change="loadData"
              class="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
        <option v-for="year in availableYears" :key="year" :value="year">
          {{ year }}年
        </option>
      </select>
    </div>

    <!-- 年度概览 -->
    <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
      <div class="bg-white p-4 rounded-lg shadow">
        <dt class="text-sm font-medium text-gray-500">年度总收入</dt>
        <dd class="mt-1 text-2xl font-semibold text-green-600">
          ¥{{ yearSummary.totalIncome.toFixed(2) }}
        </dd>
        <p class="text-xs text-gray-500 mt-1">月均 ¥{{ (yearSummary.totalIncome / 12).toFixed(2) }}</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <dt class="text-sm font-medium text-gray-500">年度总支出</dt>
        <dd class="mt-1 text-2xl font-semibold text-red-600">
          ¥{{ yearSummary.totalExpense.toFixed(2) }}
        </dd>
        <p class="text-xs text-gray-500 mt-1">月均 ¥{{ (yearSummary.totalExpense / 12).toFixed(2) }}</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <dt class="text-sm font-medium text-gray-500">年度结余</dt>
        <dd class="mt-1 text-2xl font-semibold"
            :class="yearSummary.netAmount >= 0 ? 'text-blue-600' : 'text-red-600'">
          ¥{{ yearSummary.netAmount.toFixed(2) }}
        </dd>
        <p class="text-xs text-gray-500 mt-1">储蓄率 {{ yearSummary.savingRate.toFixed(1) }}%</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <dt class="text-sm font-medium text-gray-500">最大支出月</dt>
        <dd class="mt-1 text-xl font-semibold text-gray-900">
          {{ yearSummary.maxExpenseMonth }}月
        </dd>
        <p class="text-xs text-gray-500 mt-1">¥{{ yearSummary.maxExpenseAmount.toFixed(2) }}</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <dt class="text-sm font-medium text-gray-500">最少支出月</dt>
        <dd class="mt-1 text-xl font-semibold text-gray-900">
          {{ yearSummary.minExpenseMonth }}月
        </dd>
        <p class="text-xs text-gray-500 mt-1">¥{{ yearSummary.minExpenseAmount.toFixed(2) }}</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 月度趋势图 -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-lg font-medium text-gray-900 mb-4">月度收支趋势</h2>
        <div class="h-64">
          <Line v-if="trendChartData" :data="trendChartData" :options="lineChartOptions" />
        </div>
      </div>

      <!-- 分类支出饼图 -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-lg font-medium text-gray-900 mb-4">支出分类占比</h2>
        <div class="h-64">
          <Doughnut v-if="categoryChartData" :data="categoryChartData" :options="doughnutChartOptions" />
        </div>
      </div>

      <!-- 月度对比柱状图 -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-lg font-medium text-gray-900 mb-4">月度收支对比</h2>
        <div class="h-64">
          <Bar v-if="monthlyChartData" :data="monthlyChartData" :options="barChartOptions" />
        </div>
      </div>

      <!-- 分类趋势图 -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-lg font-medium text-gray-900 mb-4">分类支出趋势</h2>
        <div class="h-64">
          <Line v-if="categoryTrendData" :data="categoryTrendData" :options="categoryLineOptions" />
        </div>
      </div>
    </div>

    <!-- 分类支出排行 -->
    <div class="mt-6 bg-white p-6 rounded-lg shadow">
      <h2 class="text-lg font-medium text-gray-900 mb-4">支出分类排行</h2>
      <div class="space-y-3">
        <div v-for="(item, index) in categoryRanking" :key="item.category"
             class="flex items-center justify-between">
          <div class="flex items-center gap-3 flex-1">
            <span class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-sm font-medium">
              {{ index + 1 }}
            </span>
            <span class="font-medium">{{ getCategoryLabel(item.category) }}</span>
            <div class="flex-1 mx-4">
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-indigo-600 h-2 rounded-full" :style="{width: `${item.percentage}%`}"></div>
              </div>
            </div>
          </div>
          <div class="text-right">
            <p class="font-semibold">¥{{ item.total.toFixed(2) }}</p>
            <p class="text-xs text-gray-500">{{ item.percentage.toFixed(1) }}% · {{ item.count }}笔</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
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

const selectedYear = ref(new Date().getFullYear())
const availableYears = ref([2024, 2025, 2026])

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

onMounted(() => {
  loadData()
})
</script>