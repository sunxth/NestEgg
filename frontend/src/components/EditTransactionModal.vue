<template>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg max-w-md w-full p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">编辑交易记录</h3>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">类型</label>
          <select
            v-model="form.type"
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
            <option value="expense">支出</option>
            <option value="income">收入</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">金额</label>
          <input
            v-model.number="form.amount"
            type="number"
            step="0.01"
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">分类</label>
          <select
            v-model="form.category"
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
            <optgroup v-if="form.type === 'expense'" label="支出分类">
              <option value="food">餐饮</option>
              <option value="transport">交通</option>
              <option value="shopping">购物</option>
              <option value="utilities">水电</option>
              <option value="entertainment">娱乐</option>
              <option value="medical">医疗</option>
              <option value="education">教育</option>
              <option value="other">其他</option>
            </optgroup>
            <optgroup v-if="form.type === 'income'" label="收入分类">
              <option value="salary">工资</option>
              <option value="bonus">奖金</option>
              <option value="other">其他</option>
            </optgroup>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">日期</label>
          <input
            v-model="form.date"
            type="datetime-local"
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">备注</label>
          <input
            v-model="form.description"
            type="text"
            maxlength="200"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        <div v-if="error" class="rounded-md bg-red-50 p-4">
          <p class="text-sm text-red-800">{{ error }}</p>
        </div>

        <div class="flex justify-end space-x-3">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            取消
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 disabled:opacity-50"
          >
            {{ loading ? '保存中...' : '保存' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTransactionStore } from '@/stores/transaction'

const props = defineProps({
  transaction: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'success'])
const transactionStore = useTransactionStore()

const loading = ref(false)
const error = ref('')

const form = ref({
  type: '',
  amount: 0,
  category: '',
  date: '',
  description: ''
})

onMounted(() => {
  if (props.transaction) {
    form.value = {
      type: props.transaction.type,
      amount: props.transaction.amount,
      category: props.transaction.category,
      date: new Date(props.transaction.date).toISOString().slice(0, 16),
      description: props.transaction.description || ''
    }
  }
})

async function handleSubmit() {
  error.value = ''
  loading.value = true

  const result = await transactionStore.updateTransaction(props.transaction.id, {
    ...form.value,
    date: new Date(form.value.date).toISOString()
  })

  if (result.success) {
    emit('success')
  } else {
    error.value = result.message
  }

  loading.value = false
}
</script>