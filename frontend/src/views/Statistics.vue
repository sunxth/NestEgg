<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-2xl font-bold text-gray-900 mb-8">统计分析</h1>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-lg font-medium text-gray-900 mb-4">月度趋势</h2>
        <div class="h-64">
          <Bar v-if="chartData.monthly" :data="chartData.monthly" :options="chartOptions" />
        </div>
      </div>

      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-lg font-medium text-gray-900 mb-4">分类统计</h2>
        <div class="h-64">
          <Pie v-if="chartData.category" :data="chartData.category" :options="pieOptions" />
        </div>
      </div>
    </div>

    <div class="mt-8 bg-white p-6 rounded-lg shadow">
      <h2 class="text-lg font-medium text-gray-900 mb-4">详细统计</h2>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                分类
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                交易次数
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                总金额
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                平均金额
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="stat in categoryStats" :key="stat.category">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ getCategoryLabel(stat.category) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ stat.count }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                ¥{{ stat.total.toFixed(2) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                ¥{{ (stat.total / stat.count).toFixed(2) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Bar, Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { useTransactionStore } from '@/stores/transaction'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

const transactionStore = useTransactionStore()

const chartData = ref({
  monthly: null,
  category: null
})

const categoryStats = ref([])

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

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    }
  }
}

const pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
    }
  }
}

function getCategoryLabel(category) {
  return categoryLabels[category] || category
}

async function loadStatistics() {
  const now = new Date()
  const year = now.getFullYear()
  const months = []
  const incomeData = []
  const expenseData = []

  for (let i = 0; i < 12; i++) {
    const result = await transactionStore.fetchMonthlyStats(year, i + 1)
    if (result.success) {
      months.push(`${i + 1}月`)
      incomeData.push(transactionStore.monthlyStats.total_income || 0)
      expenseData.push(transactionStore.monthlyStats.total_expense || 0)
    }
  }

  chartData.value.monthly = {
    labels: months,
    datasets: [
      {
        label: '收入',
        backgroundColor: '#10b981',
        data: incomeData
      },
      {
        label: '支出',
        backgroundColor: '#ef4444',
        data: expenseData
      }
    ]
  }

  const categoryResult = await transactionStore.fetchCategoryStats()
  if (categoryResult.success) {
    categoryStats.value = transactionStore.categoryStats

    chartData.value.category = {
      labels: transactionStore.categoryStats.map(s => getCategoryLabel(s.category)),
      datasets: [{
        backgroundColor: [
          '#ef4444',
          '#f97316',
          '#f59e0b',
          '#eab308',
          '#84cc16',
          '#22c55e',
          '#10b981',
          '#14b8a6',
          '#06b6d4',
          '#0ea5e9'
        ],
        data: transactionStore.categoryStats.map(s => s.total)
      }]
    }
  }
}

onMounted(() => {
  loadStatistics()
})
</script>