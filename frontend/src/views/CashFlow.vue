<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 page-fade-in">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">交易记录</h1>
      <button
        v-if="authStore.isAdmin"
        @click="showAddModal = true"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        <svg class="-ml-0.5 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        添加记录
      </button>
    </div>

    <!-- 收支汇总卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow dark:shadow-gray-700/30">
        <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">总收入</dt>
        <dd class="mt-1 text-2xl font-semibold text-green-600">
          +¥{{ summary.totalIncome.toFixed(2) }}
        </dd>
      </div>
      <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow dark:shadow-gray-700/30">
        <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">总支出</dt>
        <dd class="mt-1 text-2xl font-semibold text-red-600">
          -¥{{ summary.totalExpense.toFixed(2) }}
        </dd>
      </div>
      <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow dark:shadow-gray-700/30">
        <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">净收支</dt>
        <dd class="mt-1 text-2xl font-semibold"
            :class="summary.netAmount >= 0 ? 'text-blue-600' : 'text-red-600'">
          {{ summary.netAmount >= 0 ? '+' : '' }}¥{{ summary.netAmount.toFixed(2) }}
        </dd>
      </div>
    </div>

    <!-- 筛选器 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow dark:shadow-gray-700/30 p-4 mb-6">
      <!-- 时间和类型筛选 -->
      <div class="flex flex-wrap gap-3 mb-4">
        <!-- iOS 风格时间范围选择器 -->
        <div class="inline-flex bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
          <button
            v-for="option in timeRangeOptions"
            :key="option.value"
            @click="selectTimeRange(option.value)"
            :class="{
              'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm': timeRange === option.value,
              'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white': timeRange !== option.value
            }"
            class="px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-200"
          >
            {{ option.label }}
          </button>
        </div>

        <!-- iOS 风格类型选择器 -->
        <div class="inline-flex bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
          <button
            @click="selectTypeFilter('')"
            :class="{
              'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm': filters.type === '',
              'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white': filters.type !== ''
            }"
            class="px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-200"
          >
            全部
          </button>
          <button
            @click="selectTypeFilter('income')"
            :class="{
              'bg-white dark:bg-gray-600 text-green-600 shadow-sm': filters.type === 'income',
              'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white': filters.type !== 'income'
            }"
            class="px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-200"
          >
            收入
          </button>
          <button
            @click="selectTypeFilter('expense')"
            :class="{
              'bg-white dark:bg-gray-600 text-red-600 shadow-sm': filters.type === 'expense',
              'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white': filters.type !== 'expense'
            }"
            class="px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-200"
          >
            支出
          </button>
        </div>
      </div>

      <!-- 分类筛选（多选） -->
      <div v-if="allCategories.length > 0" class="flex items-center gap-2">
        <span class="text-sm text-gray-500 dark:text-gray-400">分类:</span>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="cat in allCategories"
            :key="cat.value"
            @click="toggleCategory(cat.value)"
            :class="{
              'bg-indigo-600 text-white': filters.categories.includes(cat.value),
              'bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600': !filters.categories.includes(cat.value)
            }"
            class="px-3 py-1 rounded-md text-sm transition-colors"
          >
            {{ cat.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- 按日期分组的交易列表 -->
    <div class="bg-white dark:bg-gray-800 shadow dark:shadow-gray-700/30 rounded-lg overflow-hidden">
      <div v-if="Object.keys(groupedTransactions).length === 0" class="px-6 py-12 text-center">
        <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">暂无交易记录</h3>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">开始添加您的第一笔交易</p>
      </div>

      <div v-else>
        <div v-for="(group, date) in groupedTransactions" :key="date" class="border-b border-gray-200 dark:border-gray-700 last:border-b-0">
          <!-- 日期标题 -->
          <div class="bg-gray-50 dark:bg-gray-700 px-6 py-3 flex justify-between items-center">
            <div class="flex items-center gap-3">
              <span class="font-medium text-gray-900 dark:text-white">{{ formatDate(date) }}</span>
              <span class="text-sm text-gray-500 dark:text-gray-400">{{ getWeekday(date) }}</span>
              <!-- 趋势图标和净收支金额 -->
              <span v-if="group.net > 0" class="inline-flex items-center gap-2 text-green-600">
                <span class="inline-flex items-center text-xs">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                  </svg>
                  净收入
                </span>
                <span class="text-base font-semibold">
                  +¥{{ Math.abs(group.net).toFixed(2) }}
                </span>
              </span>
              <span v-else-if="group.net < 0" class="inline-flex items-center gap-2 text-red-600">
                <span class="inline-flex items-center text-xs">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"/>
                  </svg>
                  净支出
                </span>
                <span class="text-base font-semibold">
                  -¥{{ Math.abs(group.net).toFixed(2) }}
                </span>
              </span>
              <span v-else class="inline-flex items-center gap-2 text-gray-500">
                <span class="inline-flex items-center text-xs">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14"/>
                  </svg>
                  持平
                </span>
                <span class="text-base font-semibold">
                  ¥0.00
                </span>
              </span>
            </div>
          </div>

          <!-- 交易列表 -->
          <ul class="divide-y divide-gray-100 dark:divide-gray-700">
            <li v-for="transaction in group.transactions" :key="transaction.id"
                class="px-6 py-3 hover:bg-gray-50 dark:hover:bg-gray-700 flex justify-between items-center">
              <div class="flex items-center gap-3 flex-1">
                <div class="flex-shrink-0 h-10 w-10 rounded-lg flex items-center justify-center"
                     :class="transaction.type === 'income' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'">
                  <svg v-if="transaction.type === 'income'" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                  <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/>
                  </svg>
                </div>
                <div class="flex-1 flex justify-between items-center">
                  <div>
                    <p class="text-sm font-medium text-gray-900 dark:text-white">{{ getCategoryLabel(transaction.category) }}</p>
                    <p class="text-xs text-gray-500 dark:text-gray-400">{{ transaction.description || '无备注' }}</p>
                  </div>
                  <span class="text-sm font-medium ml-4"
                        :class="transaction.type === 'income' ? 'text-green-600' : 'text-red-600'">
                    {{ transaction.type === 'income' ? '+' : '-' }}¥{{ transaction.amount }}
                  </span>
                </div>
              </div>

              <!-- 管理员操作按钮 -->
              <div v-if="authStore.isAdmin" class="flex items-center gap-1 ml-4">
                <button
                  @click="editTransaction(transaction)"
                  class="p-1.5 text-gray-400 dark:text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 dark:hover:bg-indigo-900/30 rounded transition-colors"
                  title="编辑"
                >
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                  </svg>
                </button>

                <!-- 删除按钮 - 内联确认 -->
                <div class="relative">
                  <button
                    v-if="deletingId !== transaction.id"
                    @click="deletingId = transaction.id"
                    class="p-1.5 text-gray-400 dark:text-gray-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded transition-colors"
                    title="删除"
                  >
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>

                  <!-- 确认删除按钮组 -->
                  <div v-else class="flex items-center gap-1 bg-white dark:bg-gray-700 rounded-lg shadow-lg border border-gray-200 dark:border-gray-600 px-2 py-1">
                    <span class="text-xs text-gray-600 dark:text-gray-300 whitespace-nowrap mr-1">确定删除?</span>
                    <button
                      @click="cancelDelete"
                      class="px-2 py-1 text-xs font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600 rounded transition-colors"
                    >
                      取消
                    </button>
                    <button
                      @click="confirmDelete(transaction.id)"
                      class="px-2 py-1 text-xs font-medium text-white bg-red-600 hover:bg-red-700 rounded transition-colors"
                    >
                      删除
                    </button>
                  </div>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 模态框 -->
    <AddTransactionModal
      v-if="showAddModal"
      @close="showAddModal = false"
      @success="handleSuccess"
    />

    <EditTransactionModal
      v-if="showEditModal"
      :transaction="editingTransaction"
      @close="showEditModal = false"
      @success="handleSuccess"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTransactionStore } from '@/stores/transaction'
import AddTransactionModal from '@/components/AddTransactionModal.vue'
import EditTransactionModal from '@/components/EditTransactionModal.vue'

const authStore = useAuthStore()
const transactionStore = useTransactionStore()

// 从 localStorage 恢复筛选状态，默认为"本周"
const savedTimeRange = localStorage.getItem('cashflow_timeRange') || 'week'
const savedType = localStorage.getItem('cashflow_type') || ''
const savedCategories = JSON.parse(localStorage.getItem('cashflow_categories') || '[]')

const timeRange = ref(savedTimeRange)
const showAddModal = ref(false)
const showEditModal = ref(false)
const editingTransaction = ref(null)
const deletingId = ref(null) // 正在删除的交易ID

const filters = ref({
  type: savedType,
  categories: savedCategories
})

const summary = ref({
  totalIncome: 0,
  totalExpense: 0,
  netAmount: 0
})

// 时间范围选项
const timeRangeOptions = [
  { value: 'week', label: '本周' },
  { value: 'month', label: '本月' },
  { value: 'quarter', label: '本季度' },
  { value: 'year', label: '本年' }
]

// 分类配置
const expenseCategories = [
  { value: 'food', label: '餐饮' },
  { value: 'transport', label: '交通' },
  { value: 'shopping', label: '购物' },
  { value: 'utilities', label: '水电' },
  { value: 'entertainment', label: '娱乐' },
  { value: 'medical', label: '医疗' },
  { value: 'education', label: '教育' },
  { value: 'other', label: '其他' }
]

const incomeCategories = [
  { value: 'salary', label: '工资' },
  { value: 'bonus', label: '奖金' },
  { value: 'other', label: '其他' }
]

// 根据类型显示对应的分类
const allCategories = computed(() => {
  if (filters.value.type === 'income') {
    return incomeCategories
  } else if (filters.value.type === 'expense') {
    return expenseCategories
  }
  return []
})

// 按日期分组的交易
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

function selectTimeRange(range) {
  timeRange.value = range
  // 保存时间范围到 localStorage
  localStorage.setItem('cashflow_timeRange', range)
  loadData()
}

function selectTypeFilter(type) {
  filters.value.type = type
  filters.value.categories = []
  // 保存状态到 localStorage
  localStorage.setItem('cashflow_type', type)
  localStorage.setItem('cashflow_categories', JSON.stringify([]))
  loadData()
}

function toggleCategory(category) {
  const index = filters.value.categories.indexOf(category)
  if (index > -1) {
    // 如果已选中，则取消选中
    filters.value.categories.splice(index, 1)
  } else {
    // 如果未选中，则添加
    filters.value.categories.push(category)
  }
  // 保存状态到 localStorage
  localStorage.setItem('cashflow_categories', JSON.stringify(filters.value.categories))
  loadData()
}

async function loadData() {
  const now = new Date()
  let startDate
  let endDate = new Date()

  switch(timeRange.value) {
    case 'week':
      startDate = new Date()
      startDate.setDate(startDate.getDate() - 7)
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

  const params = {
    start_date: startDate.toISOString(),
    end_date: endDate.toISOString()
  }

  if (filters.value.type) {
    params.type = filters.value.type
  }

  if (filters.value.categories.length > 0) {
    params.category = filters.value.categories.join(',')
  }

  await transactionStore.fetchTransactions(params)

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

  summary.value = {
    totalIncome,
    totalExpense,
    netAmount: totalIncome - totalExpense
  }
}

function editTransaction(transaction) {
  editingTransaction.value = transaction
  showEditModal.value = true
}

function cancelDelete() {
  deletingId.value = null
}

async function confirmDelete(id) {
  const result = await transactionStore.deleteTransaction(id)
  if (result.success) {
    deletingId.value = null
    loadData()
  } else {
    alert(result.message)
    deletingId.value = null
  }
}

function handleSuccess() {
  showAddModal.value = false
  showEditModal.value = false
  editingTransaction.value = null
  loadData()
}

onMounted(() => {
  loadData()
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