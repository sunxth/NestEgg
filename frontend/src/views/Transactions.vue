<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">交易记录</h1>
      <button
        v-if="authStore.isAdmin"
        @click="showAddModal = true"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
      >
        添加记录
      </button>
    </div>

    <div class="bg-white shadow overflow-hidden sm:rounded-md">
      <div class="px-4 py-3 border-b border-gray-200 sm:px-6">
        <div class="flex flex-wrap gap-4">
          <select
            v-model="filters.type"
            @change="loadTransactions"
            class="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
            <option value="">所有类型</option>
            <option value="income">收入</option>
            <option value="expense">支出</option>
            <option value="deposit">存款</option>
          </select>

          <select
            v-model="filters.category"
            @change="loadTransactions"
            class="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
            <option value="">所有分类</option>
            <option value="food">餐饮</option>
            <option value="transport">交通</option>
            <option value="shopping">购物</option>
            <option value="utilities">水电</option>
            <option value="entertainment">娱乐</option>
            <option value="medical">医疗</option>
            <option value="education">教育</option>
            <option value="salary">工资</option>
            <option value="bonus">奖金</option>
            <option value="deposit">存款</option>
            <option value="other">其他</option>
          </select>
        </div>
      </div>

      <ul class="divide-y divide-gray-200">
        <li v-for="transaction in transactionStore.transactions" :key="transaction.id"
            class="px-6 py-4 hover:bg-gray-50">
          <div class="flex items-center justify-between">
            <div class="flex items-center flex-1">
              <div class="flex-shrink-0 h-10 w-10 rounded-full flex items-center justify-center"
                   :class="transaction.type === 'income' ? 'bg-green-100' : transaction.type === 'deposit' ? 'bg-blue-100' : 'bg-red-100'">
                <span :class="transaction.type === 'income' ? 'text-green-800' : transaction.type === 'deposit' ? 'text-blue-800' : 'text-red-800'">
                  {{ transaction.type === 'income' ? '+' : transaction.type === 'deposit' ? '↓' : '-' }}
                </span>
              </div>
              <div class="ml-4 flex-1">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm font-medium text-gray-900">
                      {{ getCategoryLabel(transaction.category) }}
                    </p>
                    <p class="text-sm text-gray-500">
                      {{ transaction.description || '无备注' }}
                    </p>
                  </div>
                  <div class="text-right">
                    <p class="text-sm font-medium"
                       :class="transaction.type === 'income' ? 'text-green-600' : transaction.type === 'deposit' ? 'text-blue-600' : 'text-red-600'">
                      {{ transaction.type === 'income' ? '+' : transaction.type === 'deposit' ? '↓' : '-' }}¥{{ transaction.amount }}
                    </p>
                    <p class="text-sm text-gray-500">
                      {{ new Date(transaction.date).toLocaleDateString() }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="authStore.isAdmin" class="ml-4 flex space-x-2">
              <button
                @click="editTransaction(transaction)"
                class="text-indigo-600 hover:text-indigo-900 text-sm"
              >
                编辑
              </button>
              <button
                @click="deleteTransaction(transaction.id)"
                class="text-red-600 hover:text-red-900 text-sm"
              >
                删除
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTransactionStore } from '@/stores/transaction'
import AddTransactionModal from '@/components/AddTransactionModal.vue'
import EditTransactionModal from '@/components/EditTransactionModal.vue'

const authStore = useAuthStore()
const transactionStore = useTransactionStore()

const showAddModal = ref(false)
const showEditModal = ref(false)
const editingTransaction = ref(null)

const filters = ref({
  type: '',
  category: ''
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

async function loadTransactions() {
  const params = {}
  if (filters.value.type) params.type = filters.value.type
  if (filters.value.category) params.category = filters.value.category
  await transactionStore.fetchTransactions(params)
}

function editTransaction(transaction) {
  editingTransaction.value = transaction
  showEditModal.value = true
}

async function deleteTransaction(id) {
  if (confirm('确定要删除这条记录吗？')) {
    await transactionStore.deleteTransaction(id)
  }
}

function handleAddSuccess() {
  showAddModal.value = false
  loadTransactions()
}

function handleEditSuccess() {
  showEditModal.value = false
  loadTransactions()
}

onMounted(() => {
  loadTransactions()
})
</script>