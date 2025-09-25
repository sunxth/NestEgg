<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">日历视图</h1>
      <div class="flex gap-2">
        <button @click="previousMonth"
                class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
          </svg>
        </button>
        <div class="px-4 py-2 font-medium text-gray-900">
          {{ currentYear }}年{{ currentMonth }}月
        </div>
        <button @click="nextMonth"
                class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
          </svg>
        </button>
        <button @click="goToToday"
                class="ml-2 px-4 py-2 text-sm text-indigo-600 hover:bg-indigo-50 rounded-lg">
          今天
        </button>
      </div>
    </div>

    <!-- 月度统计 -->
    <div class="grid grid-cols-3 gap-4 mb-6">
      <div class="bg-white p-4 rounded-lg shadow">
        <dt class="text-sm font-medium text-gray-500">本月收入</dt>
        <dd class="mt-1 text-xl font-semibold text-green-600">
          +¥{{ monthSummary.income.toFixed(2) }}
        </dd>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <dt class="text-sm font-medium text-gray-500">本月支出</dt>
        <dd class="mt-1 text-xl font-semibold text-red-600">
          -¥{{ monthSummary.expense.toFixed(2) }}
        </dd>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <dt class="text-sm font-medium text-gray-500">本月结余</dt>
        <dd class="mt-1 text-xl font-semibold"
            :class="monthSummary.net >= 0 ? 'text-blue-600' : 'text-red-600'">
          {{ monthSummary.net >= 0 ? '+' : '' }}¥{{ monthSummary.net.toFixed(2) }}
        </dd>
      </div>
    </div>

    <!-- 日历表格 -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="grid grid-cols-7">
        <div v-for="day in weekDays" :key="day"
             class="py-3 text-center text-sm font-medium text-gray-900 bg-gray-50 border-b">
          {{ day }}
        </div>
      </div>
      <div class="grid grid-cols-7">
        <div v-for="(date, index) in calendarDates" :key="index"
             class="min-h-[100px] p-2 border-b border-r"
             :class="getDateClass(date)">
          <div v-if="date">
            <div class="flex justify-between items-start mb-1">
              <span class="text-sm font-medium"
                    :class="isToday(date) ? 'text-white bg-indigo-600 rounded-full w-6 h-6 flex items-center justify-center' : 'text-gray-900'">
                {{ date.getDate() }}
              </span>
              <span v-if="getDateSummary(date).net !== 0"
                    class="text-xs font-medium"
                    :class="getDateSummary(date).net >= 0 ? 'text-green-600' : 'text-red-600'">
                {{ getDateSummary(date).net >= 0 ? '+' : '' }}{{ getDateSummary(date).net.toFixed(0) }}
              </span>
            </div>
            <div class="space-y-1">
              <div v-for="transaction in getDateTransactions(date).slice(0, 3)"
                   :key="transaction.id"
                   class="text-xs truncate"
                   :class="transaction.type === 'income' ? 'text-green-600' : 'text-red-600'">
                <span>{{ transaction.type === 'income' ? '+' : '-' }}{{ parseFloat(transaction.amount).toFixed(0) }}</span>
                <span class="text-gray-500 ml-1">{{ getCategoryLabel(transaction.category) }}</span>
              </div>
              <div v-if="getDateTransactions(date).length > 3"
                   class="text-xs text-gray-400">
                还有{{ getDateTransactions(date).length - 3 }}笔...
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 选中日期的详细交易 -->
    <div v-if="selectedDate" class="mt-6 bg-white rounded-lg shadow p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">
        {{ formatDate(selectedDate) }} 交易明细
      </h3>
      <ul class="divide-y divide-gray-200">
        <li v-for="transaction in getDateTransactions(selectedDate)"
            :key="transaction.id"
            class="py-3 flex justify-between items-center">
          <div>
            <p class="text-sm font-medium text-gray-900">{{ getCategoryLabel(transaction.category) }}</p>
            <p class="text-sm text-gray-500">{{ transaction.description || '无备注' }}</p>
          </div>
          <span class="text-sm font-medium"
                :class="transaction.type === 'income' ? 'text-green-600' : 'text-red-600'">
            {{ transaction.type === 'income' ? '+' : '-' }}¥{{ transaction.amount }}
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTransactionStore } from '@/stores/transaction'

const transactionStore = useTransactionStore()

const currentDate = ref(new Date())
const selectedDate = ref(null)

const weekDays = ['日', '一', '二', '三', '四', '五', '六']

const currentYear = computed(() => currentDate.value.getFullYear())
const currentMonth = computed(() => currentDate.value.getMonth() + 1)

const calendarDates = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const startPadding = firstDay.getDay()
  const dates = []

  // 添加空白日期
  for (let i = 0; i < startPadding; i++) {
    dates.push(null)
  }

  // 添加当月日期
  for (let i = 1; i <= lastDay.getDate(); i++) {
    dates.push(new Date(year, month, i))
  }

  // 补齐到42个格子（6行）
  while (dates.length < 42) {
    dates.push(null)
  }

  return dates
})

const monthSummary = computed(() => {
  let income = 0
  let expense = 0

  transactionStore.transactions.forEach(t => {
    const tDate = new Date(t.date)
    if (tDate.getFullYear() === currentYear.value && tDate.getMonth() + 1 === currentMonth.value) {
      if (t.type === 'income') {
        income += parseFloat(t.amount)
      } else {
        expense += parseFloat(t.amount)
      }
    }
  })

  return {
    income,
    expense,
    net: income - expense
  }
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

function getDateTransactions(date) {
  if (!date) return []
  const dateStr = date.toISOString().split('T')[0]
  return transactionStore.transactions.filter(t => {
    return t.date.startsWith(dateStr)
  })
}

function getDateSummary(date) {
  const transactions = getDateTransactions(date)
  let income = 0
  let expense = 0

  transactions.forEach(t => {
    if (t.type === 'income') {
      income += parseFloat(t.amount)
    } else {
      expense += parseFloat(t.amount)
    }
  })

  return { income, expense, net: income - expense }
}

function getDateClass(date) {
  if (!date) return 'bg-gray-50'
  const classes = ['bg-white hover:bg-gray-50 cursor-pointer']

  if (isToday(date)) {
    classes.push('ring-2 ring-indigo-500')
  }

  const summary = getDateSummary(date)
  if (summary.net > 0) {
    classes.push('border-l-4 border-l-green-500')
  } else if (summary.net < 0) {
    classes.push('border-l-4 border-l-red-500')
  }

  return classes.join(' ')
}

function isToday(date) {
  if (!date) return false
  const today = new Date()
  return date.toDateString() === today.toDateString()
}

function formatDate(date) {
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
}

function previousMonth() {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1)
  loadData()
}

function nextMonth() {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1)
  loadData()
}

function goToToday() {
  currentDate.value = new Date()
  loadData()
}

async function loadData() {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  const startDate = new Date(year, month, 1)
  const endDate = new Date(year, month + 1, 0)

  await transactionStore.fetchTransactions({
    start_date: startDate,
    end_date: endDate
  })
}

onMounted(() => {
  loadData()
})
</script>