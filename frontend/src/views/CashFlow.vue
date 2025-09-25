<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">收支明细</h1>
      <div class="flex gap-4">
        <select v-model="timeRange" @change="loadData"
                class="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
          <option value="week">本周</option>
          <option value="month">本月</option>
          <option value="quarter">本季度</option>
          <option value="year">本年</option>
        </select>
      </div>
    </div>

    <!-- 收支汇总卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-white p-4 rounded-lg shadow">
        <dt class="text-sm font-medium text-gray-500">总收入</dt>
        <dd class="mt-1 text-2xl font-semibold text-green-600">
          +¥{{ summary.totalIncome.toFixed(2) }}
        </dd>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <dt class="text-sm font-medium text-gray-500">总支出</dt>
        <dd class="mt-1 text-2xl font-semibold text-red-600">
          -¥{{ summary.totalExpense.toFixed(2) }}
        </dd>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <dt class="text-sm font-medium text-gray-500">净收支</dt>
        <dd class="mt-1 text-2xl font-semibold"
            :class="summary.netAmount >= 0 ? 'text-blue-600' : 'text-red-600'">
          {{ summary.netAmount >= 0 ? '+' : '' }}¥{{ summary.netAmount.toFixed(2) }}
        </dd>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <dt class="text-sm font-medium text-gray-500">日均支出</dt>
        <dd class="mt-1 text-2xl font-semibold text-gray-900">
          ¥{{ summary.dailyAverage.toFixed(2) }}
        </dd>
      </div>
    </div>

    <!-- 按日期分组的收支列表 -->
    <div class="bg-white shadow rounded-lg overflow-hidden">
      <div v-for="(group, date) in groupedTransactions" :key="date" class="border-b border-gray-200 last:border-b-0">
        <div class="bg-gray-50 px-6 py-3 flex justify-between items-center">
          <div class="flex items-center gap-4">
            <span class="font-medium text-gray-900">{{ formatDate(date) }}</span>
            <span class="text-sm text-gray-500">{{ getWeekday(date) }}</span>
          </div>
          <div class="flex gap-4 text-sm">
            <span class="text-green-600">+¥{{ group.income.toFixed(2) }}</span>
            <span class="text-red-600">-¥{{ group.expense.toFixed(2) }}</span>
            <span class="font-medium" :class="group.net >= 0 ? 'text-blue-600' : 'text-red-600'">
              {{ group.net >= 0 ? '+' : '' }}¥{{ group.net.toFixed(2) }}
            </span>
          </div>
        </div>
        <ul class="divide-y divide-gray-200">
          <li v-for="transaction in group.transactions" :key="transaction.id"
              class="px-6 py-3 hover:bg-gray-50 flex justify-between items-center">
            <div class="flex items-center gap-3">
              <div class="flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center text-xs"
                   :class="transaction.type === 'income' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                {{ transaction.type === 'income' ? '+' : '-' }}
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900">{{ getCategoryLabel(transaction.category) }}</p>
                <p class="text-xs text-gray-500">{{ transaction.description || '无备注' }}</p>
              </div>
            </div>
            <span class="text-sm font-medium"
                  :class="transaction.type === 'income' ? 'text-green-600' : 'text-red-600'">
              {{ transaction.type === 'income' ? '+' : '-' }}¥{{ transaction.amount }}
            </span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useTransactionStore } from '@/stores/transaction'

const transactionStore = useTransactionStore()
const timeRange = ref('month')

const summary = ref({
  totalIncome: 0,
  totalExpense: 0,
  netAmount: 0,
  dailyAverage: 0
})

const groupedTransactions = computed(() => {
  const groups = {}

  transactionStore.transactions.forEach(transaction => {
    const dateKey = new Date(transaction.date).toISOString().split('T')[0]
    if (!groups[dateKey]) {
      groups[dateKey] = {
        transactions: [],
        income: 0,
        expense: 0,
        net: 0
      }
    }

    groups[dateKey].transactions.push(transaction)
    if (transaction.type === 'income') {
      groups[dateKey].income += parseFloat(transaction.amount)
    } else {
      groups[dateKey].expense += parseFloat(transaction.amount)
    }
    groups[dateKey].net = groups[dateKey].income - groups[dateKey].expense
  })

  return Object.keys(groups)
    .sort((a, b) => new Date(b) - new Date(a))
    .reduce((acc, key) => {
      acc[key] = groups[key]
      return acc
    }, {})
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

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

function getWeekday(dateStr) {
  const days = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  return days[new Date(dateStr).getDay()]
}

async function loadData() {
  const now = new Date()
  let startDate, endDate = now

  switch(timeRange.value) {
    case 'week':
      startDate = new Date(now.setDate(now.getDate() - 7))
      break
    case 'month':
      startDate = new Date(now.getFullYear(), now.getMonth(), 1)
      break
    case 'quarter':
      const quarter = Math.floor(now.getMonth() / 3)
      startDate = new Date(now.getFullYear(), quarter * 3, 1)
      break
    case 'year':
      startDate = new Date(now.getFullYear(), 0, 1)
      break
  }

  await transactionStore.fetchTransactions({ start_date: startDate, end_date: endDate })

  // 计算汇总数据
  let totalIncome = 0
  let totalExpense = 0

  transactionStore.transactions.forEach(t => {
    if (t.type === 'income') {
      totalIncome += parseFloat(t.amount)
    } else {
      totalExpense += parseFloat(t.amount)
    }
  })

  const days = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) || 1

  summary.value = {
    totalIncome,
    totalExpense,
    netAmount: totalIncome - totalExpense,
    dailyAverage: totalExpense / days
  }
}

onMounted(() => {
  loadData()
})
</script>