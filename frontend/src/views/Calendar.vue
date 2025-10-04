<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 page-fade-in">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">日历视图</h1>
      <div class="flex gap-2 items-center">
        <button @click="previousMonth"
                class="p-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
          </svg>
        </button>

        <!-- Month/Year Picker -->
        <div class="relative">
          <button
            @click="showMonthPicker = !showMonthPicker"
            class="px-4 py-2 font-medium text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
            </svg>
            <span>{{ currentYear }}年{{ currentMonth }}月</span>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"
                 class="w-4 h-4 transition-transform duration-200"
                 :class="{'rotate-180': showMonthPicker}">
              <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
            </svg>
          </button>

          <!-- Month Picker Dropdown -->
          <Transition
            enter-active-class="transition duration-100 ease-out"
            enter-from-class="opacity-0 scale-95"
            enter-to-class="opacity-100 scale-100"
            leave-active-class="transition duration-75 ease-in"
            leave-from-class="opacity-100 scale-100"
            leave-to-class="opacity-0 scale-95"
          >
            <div
              v-if="showMonthPicker"
              class="absolute z-10 mt-2 w-80 bg-white dark:bg-gray-800 rounded-2xl shadow-xl dark:shadow-gray-700/30 border border-gray-200 dark:border-gray-700 p-4"
            >
              <!-- Year selector -->
              <div class="flex items-center justify-between mb-4">
                <button
                  @click.stop="pickerYear--"
                  class="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
                  </svg>
                </button>

                <span class="text-base font-semibold text-gray-900 dark:text-white">{{ pickerYear }}年</span>

                <button
                  @click.stop="pickerYear++"
                  :disabled="pickerYear >= new Date().getFullYear()"
                  :class="{'opacity-30 cursor-not-allowed': pickerYear >= new Date().getFullYear()}"
                  class="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors disabled:hover:bg-transparent"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                  </svg>
                </button>
              </div>

              <!-- Month grid -->
              <div class="grid grid-cols-3 gap-2">
                <button
                  v-for="month in 12"
                  :key="month"
                  @click.stop="selectMonth(month)"
                  :disabled="isMonthDisabled(pickerYear, month)"
                  :class="{
                    'bg-indigo-600 text-white font-semibold': currentYear === pickerYear && currentMonth === month,
                    'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-900 dark:text-white': !(currentYear === pickerYear && currentMonth === month) && !isMonthDisabled(pickerYear, month),
                    'bg-gray-50 dark:bg-gray-700 text-gray-300 cursor-not-allowed': isMonthDisabled(pickerYear, month)
                  }"
                  class="py-3 px-4 rounded-lg text-sm font-medium transition-colors"
                >
                  {{ month }}月
                </button>
              </div>
            </div>
          </Transition>
        </div>

        <button @click="nextMonth"
                class="p-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
          </svg>
        </button>
        <button @click="goToToday"
                class="ml-2 px-4 py-2 text-sm text-indigo-600 hover:bg-indigo-50 dark:hover:bg-indigo-900/30 rounded-lg transition-colors">
          今天
        </button>
      </div>
    </div>

    <!-- 月度统计 -->
    <div class="grid grid-cols-3 gap-4 mb-6">
      <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow dark:shadow-gray-700/30">
        <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">本月收入</dt>
        <dd class="mt-1 text-xl font-semibold text-green-600">
          +¥{{ monthSummary.income.toFixed(2) }}
        </dd>
      </div>
      <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow dark:shadow-gray-700/30">
        <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">本月支出</dt>
        <dd class="mt-1 text-xl font-semibold text-red-600">
          -¥{{ monthSummary.expense.toFixed(2) }}
        </dd>
      </div>
      <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow dark:shadow-gray-700/30">
        <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">本月结余</dt>
        <dd class="mt-1 text-xl font-semibold"
            :class="monthSummary.net >= 0 ? 'text-blue-600' : 'text-red-600'">
          {{ monthSummary.net >= 0 ? '+' : '' }}¥{{ monthSummary.net.toFixed(2) }}
        </dd>
      </div>
    </div>

    <!-- 日历表格 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow dark:shadow-gray-700/30 overflow-hidden">
      <div class="grid grid-cols-7">
        <div v-for="day in weekDays" :key="day"
             class="py-3 text-center text-sm font-medium text-gray-900 dark:text-white bg-gray-50 dark:bg-gray-700 border-b dark:border-gray-700">
          {{ day }}
        </div>
      </div>
      <div class="grid grid-cols-7">
        <div v-for="(date, index) in calendarDates" :key="index"
             class="min-h-[100px] p-2 border-b border-r dark:border-gray-700"
             :class="getDateClass(date)">
          <div v-if="date">
            <div class="flex justify-between items-start mb-1">
              <span class="text-sm font-medium"
                    :class="isToday(date) ? 'text-white bg-indigo-600 rounded-full w-6 h-6 flex items-center justify-center' : 'text-gray-900 dark:text-white'">
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
                <span class="text-gray-500 dark:text-gray-400 ml-1">{{ getCategoryLabel(transaction.category) }}</span>
              </div>
              <div v-if="getDateTransactions(date).length > 3"
                   class="text-xs text-gray-400 dark:text-gray-500">
                还有{{ getDateTransactions(date).length - 3 }}笔...
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 选中日期的详细交易 -->
    <div v-if="selectedDate" class="mt-6 bg-white dark:bg-gray-800 rounded-lg shadow dark:shadow-gray-700/30 p-6">
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
        {{ formatDate(selectedDate) }} 交易明细
      </h3>
      <ul class="divide-y divide-gray-200 dark:divide-gray-700">
        <li v-for="transaction in getDateTransactions(selectedDate)"
            :key="transaction.id"
            class="py-3 flex justify-between items-center">
          <div>
            <p class="text-sm font-medium text-gray-900 dark:text-white">{{ getCategoryLabel(transaction.category) }}</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">{{ transaction.description || '无备注' }}</p>
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
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useTransactionStore } from '@/stores/transaction'

const transactionStore = useTransactionStore()

const currentDate = ref(new Date())
const selectedDate = ref(null)
const showMonthPicker = ref(false)
const pickerYear = ref(new Date().getFullYear())

const weekDays = ['日', '一', '二', '三', '四', '五', '六']

// Watch currentDate to update pickerYear
watch(currentDate, (newDate) => {
  pickerYear.value = newDate.getFullYear()
})

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
  if (!date) return 'bg-gray-50 dark:bg-gray-900'
  const classes = ['bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer']

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

function isMonthDisabled(year, month) {
  const today = new Date()
  const currentYearNow = today.getFullYear()
  const currentMonthNow = today.getMonth() + 1

  if (year > currentYearNow) return true
  if (year === currentYearNow && month > currentMonthNow) return true
  return false
}

function selectMonth(month) {
  if (isMonthDisabled(pickerYear.value, month)) return

  currentDate.value = new Date(pickerYear.value, month - 1, 1)
  showMonthPicker.value = false
  loadData()
}

// Close month picker when clicking outside
function handleClickOutside(event) {
  const target = event.target
  if (!target.closest('.relative')) {
    showMonthPicker.value = false
  }
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
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* 页面淡入动画 */
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
</style>