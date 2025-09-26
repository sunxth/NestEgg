<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex justify-between items-end">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">交易记录</h1>
            <p class="mt-1 text-sm text-gray-500">{{ new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long' }) }}</p>
          </div>
          <button
            v-if="authStore.isAdmin"
            @click="showAddModal = true"
            class="inline-flex items-center px-5 py-2.5 border border-transparent text-sm font-medium rounded-full shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200"
          >
            <svg class="-ml-0.5 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            添加记录
          </button>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-white rounded-2xl shadow-sm p-6 mb-6">
        <!-- 类型筛选 -->
        <div class="mb-4">
          <div class="flex flex-wrap gap-2">
            <button
              @click="selectAllTypes"
              :class="{
                'bg-indigo-600 text-white': filters.type === '',
                'bg-gray-100 text-gray-700 hover:bg-gray-200': filters.type !== ''
              }"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-150"
            >
              所有类型
            </button>
            <button
              @click="filters.type = 'income'"
              :class="{
                'bg-green-600 text-white': filters.type === 'income',
                'bg-gray-100 text-gray-700 hover:bg-gray-200': filters.type !== 'income'
              }"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-150"
            >
              收入
            </button>
            <button
              @click="filters.type = 'expense'"
              :class="{
                'bg-red-600 text-white': filters.type === 'expense',
                'bg-gray-100 text-gray-700 hover:bg-gray-200': filters.type !== 'expense'
              }"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-150"
            >
              支出
            </button>
          </div>
        </div>

        <!-- 分类筛选 -->
        <div v-if="visibleCategories.length > 0">
          <div class="flex flex-wrap gap-2">
            <button
              v-for="cat in visibleCategories"
              :key="cat.value"
              @click="filters.category = filters.category === cat.value ? '' : cat.value"
              :class="{
                'bg-indigo-600 text-white': filters.category === cat.value,
                'bg-gray-100 text-gray-700 hover:bg-gray-200': filters.category !== cat.value
              }"
              class="inline-flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-150"
            >
              <component :is="cat.icon" class="w-4 h-4 mr-1.5" />
              {{ cat.label }}
            </button>
          </div>
        </div>
      </div>

      <!-- Transaction List -->
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden">

        <div v-if="transactionStore.transactions.length === 0" class="px-6 py-12 text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">暂无交易记录</h3>
          <p class="mt-1 text-sm text-gray-500">开始添加您的第一笔交易</p>
        </div>

        <ul v-else class="divide-y divide-gray-100">
          <li v-for="transaction in transactionStore.transactions" :key="transaction.id"
              class="px-6 py-4 hover:bg-gray-50 transition-colors duration-150">
            <div class="flex items-center">
              <!-- Icon -->
              <div class="flex-shrink-0 h-12 w-12 rounded-2xl flex items-center justify-center"
                   :class="{
                     'bg-green-50': transaction.type === 'income',
                     'bg-red-50': transaction.type === 'expense'
                   }">
                <svg v-if="transaction.type === 'income'" class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                <svg v-else class="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/>
                </svg>
              </div>

              <!-- Content -->
              <div class="ml-4 flex-1">
                <div class="flex items-center justify-between">
                  <div>
                    <div class="flex items-center">
                      <p class="text-base font-semibold text-gray-900">
                        {{ getCategoryLabel(transaction.category) }}
                      </p>
                      <span class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                            :class="{
                              'bg-green-100 text-green-800': transaction.type === 'income',
                              'bg-red-100 text-red-800': transaction.type === 'expense'
                            }">
                        {{ transaction.type === 'income' ? '收入' : '支出' }}
                      </span>
                    </div>
                    <p class="mt-1 text-sm text-gray-500">
                      {{ transaction.description || '无备注' }}
                    </p>
                  </div>
                  <div class="text-right">
                    <p class="text-lg font-semibold"
                       :class="{
                         'text-green-600': transaction.type === 'income',
                         'text-red-600': transaction.type === 'expense'
                       }">
                      {{ transaction.type === 'income' ? '+' : '-' }}¥{{ Number(transaction.amount).toFixed(2) }}
                    </p>
                    <p class="text-xs text-gray-500 mt-1">
                      {{ new Date(transaction.date).toLocaleDateString('zh-CN') }}
                    </p>
                  </div>
                </div>
              </div>

              <!-- Actions -->
              <div v-if="authStore.isAdmin" class="ml-6 flex items-center space-x-1">
                <button
                  @click="editTransaction(transaction)"
                  class="p-2 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                  title="编辑"
                >
                  <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                  </svg>
                </button>
                <button
                  @click="deleteTransaction(transaction.id)"
                  class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                  title="删除"
                >
                  <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                </button>
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

      <EditTransactionModal
        v-if="showEditModal"
        :transaction="editingTransaction"
        @close="showEditModal = false"
        @success="handleEditSuccess"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTransactionStore } from '@/stores/transaction'
import AddTransactionModal from '@/components/AddTransactionModal.vue'
import EditTransactionModal from '@/components/EditTransactionModal.vue'
import {
  Squares2X2Icon,
  TruckIcon,
  ShoppingBagIcon,
  BoltIcon,
  FilmIcon,
  HeartIcon,
  AcademicCapIcon,
  FolderIcon,
  BanknotesIcon,
  GiftIcon
} from '@heroicons/vue/24/outline'

const authStore = useAuthStore()
const transactionStore = useTransactionStore()

const showAddModal = ref(false)
const showEditModal = ref(false)
const editingTransaction = ref(null)

const filters = ref({
  type: '',
  category: ''
})

// 支出分类配置
const expenseCategories = [
  { value: 'food', label: '餐饮', icon: Squares2X2Icon, type: 'expense' },
  { value: 'transport', label: '交通', icon: TruckIcon, type: 'expense' },
  { value: 'shopping', label: '购物', icon: ShoppingBagIcon, type: 'expense' },
  { value: 'utilities', label: '水电', icon: BoltIcon, type: 'expense' },
  { value: 'entertainment', label: '娱乐', icon: FilmIcon, type: 'expense' },
  { value: 'medical', label: '医疗', icon: HeartIcon, type: 'expense' },
  { value: 'education', label: '教育', icon: AcademicCapIcon, type: 'expense' },
  { value: 'other', label: '其他', icon: FolderIcon, type: 'expense' }
]

// 收入分类配置
const incomeCategories = [
  { value: 'salary', label: '工资', icon: BanknotesIcon, type: 'income' },
  { value: 'bonus', label: '奖金', icon: GiftIcon, type: 'income' },
  { value: 'other', label: '其他', icon: FolderIcon, type: 'income' }
]

// 根据类型筛选动态显示分类
const visibleCategories = computed(() => {
  if (filters.value.type === 'income') {
    return incomeCategories
  } else if (filters.value.type === 'expense') {
    return expenseCategories
  } else {
    // 所有类型时，显示所有分类
    return [...expenseCategories, ...incomeCategories]
  }
})

// 监听类型变化，自动清除不匹配的分类
watch(() => filters.value.type, (newType, oldType) => {
  // 当切换类型时，如果当前选择的分类不属于新类型，则清空分类筛选
  if (newType && filters.value.category) {
    const categoryValid = visibleCategories.value.some(cat => cat.value === filters.value.category)
    if (!categoryValid) {
      filters.value.category = ''
    }
  }
})

// 监听筛选变化
watch(filters, () => {
  loadTransactions()
}, { deep: true })

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

// 选择"所有类型"时，清除分类筛选
function selectAllTypes() {
  filters.value.type = ''
  filters.value.category = ''
}

async function loadTransactions() {
  await transactionStore.fetchTransactions(filters.value)
}

function editTransaction(transaction) {
  editingTransaction.value = transaction
  showEditModal.value = true
}

async function deleteTransaction(id) {
  if (confirm('确定要删除这条记录吗？')) {
    const result = await transactionStore.deleteTransaction(id)
    if (result.success) {
      loadTransactions()
    } else {
      alert(result.message)
    }
  }
}

function handleAddSuccess() {
  showAddModal.value = false
  loadTransactions()
}

function handleEditSuccess() {
  showEditModal.value = false
  editingTransaction.value = null
  loadTransactions()
}

onMounted(() => {
  loadTransactions()
})
</script>