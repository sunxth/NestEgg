<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">交易记录</h1>
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
    </div>

    <!-- 筛选器 -->
    <div class="bg-white rounded-lg shadow p-4 mb-6">
      <!-- 时间和类型筛选 -->
      <div class="flex flex-wrap gap-3 mb-4">
        <select v-model="timeRange" @change="loadData"
                class="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
          <option value="week">本周</option>
          <option value="month">本月</option>
          <option value="quarter">本季度</option>
          <option value="year">本年</option>
        </select>

        <div class="flex gap-2">
          <button
            @click="selectTypeFilter('')"
            :class="{
              'bg-indigo-600 text-white': filters.type === '',
              'bg-gray-100 text-gray-700 hover:bg-gray-200': filters.type !== ''
            }"
            class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
          >
            全部
          </button>
          <button
            @click="selectTypeFilter('income')"
            :class="{
              'bg-green-600 text-white': filters.type === 'income',
              'bg-gray-100 text-gray-700 hover:bg-gray-200': filters.type !== 'income'
            }"
            class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
          >
            收入
          </button>
          <button
            @click="selectTypeFilter('expense')"
            :class="{
              'bg-red-600 text-white': filters.type === 'expense',
              'bg-gray-100 text-gray-700 hover:bg-gray-200': filters.type !== 'expense'
            }"
            class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
          >
            支出
          </button>
        </div>
      </div>

      <!-- 分类筛选（多选） -->
      <div v-if="allCategories.length > 0" class="flex items-center gap-2">
        <span class="text-sm text-gray-500">分类:</span>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="cat in allCategories"
            :key="cat.value"
            @click="toggleCategory(cat.value)"
            :class="{
              'bg-indigo-600 text-white': filters.categories.includes(cat.value),
              'bg-gray-50 text-gray-700 hover:bg-gray-100': !filters.categories.includes(cat.value)
            }"
            class="px-3 py-1 rounded-md text-sm transition-colors"
          >
            {{ cat.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- 按日期分组的交易列表 -->
    <div class="bg-white shadow rounded-lg overflow-hidden">
      <div v-if="Object.keys(groupedTransactions).length === 0" class="px-6 py-12 text-center">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">暂无交易记录</h3>
        <p class="mt-1 text-sm text-gray-500">开始添加您的第一笔交易</p>
      </div>

      <div v-else>
        <div v-for="(group, date) in groupedTransactions" :key="date" class="border-b border-gray-200 last:border-b-0">
          <!-- 日期标题 -->
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

          <!-- 交易列表 -->
          <ul class="divide-y divide-gray-100">
            <li v-for="transaction in group.transactions" :key="transaction.id"
                class="px-6 py-3 hover:bg-gray-50 flex justify-between items-center">
              <div class="flex items-center gap-3">
                <div class="flex-shrink-0 h-10 w-10 rounded-lg flex items-center justify-center"
                     :class="transaction.type === 'income' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'">
                  <svg v-if="transaction.type === 'income'" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                  <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/>
                  </svg>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ getCategoryLabel(transaction.category) }}</p>
                  <p class="text-xs text-gray-500">{{ transaction.description || '无备注' }}</p>
                </div>
              </div>

              <div class="flex items-center gap-4">
                <span class="text-sm font-semibold"
                      :class="transaction.type === 'income' ? 'text-green-600' : 'text-red-600'">
                  {{ transaction.type === 'income' ? '+' : '-' }}¥{{ transaction.amount }}
                </span>

                <!-- 管理员操作按钮 -->
                <div v-if="authStore.isAdmin" class="flex items-center gap-1">
                  <button
                    @click="editTransaction(transaction)"
                    class="p-1.5 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 rounded transition-colors"
                    title="编辑"
                  >
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </button>
                  <button
                    @click="deleteTransaction(transaction.id)"
                    class="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
                    title="删除"
                  >
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
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

const timeRange = ref('month')
const showAddModal = ref(false)
const showEditModal = ref(false)
const editingTransaction = ref(null)

const filters = ref({
  type: '',
  categories: [] // 改为数组支持多选
})

const summary = ref({
  totalIncome: 0,
  totalExpense: 0,
  netAmount: 0
})

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

function selectTypeFilter(type) {
  filters.value.type = type
  filters.value.categories = []
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

async function deleteTransaction(id) {
  if (confirm('确定要删除这条记录吗？')) {
    const result = await transactionStore.deleteTransaction(id)
    if (result.success) {
      loadData()
    } else {
      alert(result.message)
    }
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