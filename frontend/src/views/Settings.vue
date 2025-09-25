<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-2xl font-bold text-gray-900 mb-8">设置</h1>

    <div class="bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">数据导出</h3>

        <div class="space-y-4">
          <div>
            <button
              @click="exportCSV"
              class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              导出 CSV 文件
            </button>
            <p class="mt-2 text-sm text-gray-500">
              将所有交易记录导出为 CSV 格式文件
            </p>
          </div>

          <div>
            <button
              @click="exportDatabase"
              class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              备份数据库
            </button>
            <p class="mt-2 text-sm text-gray-500">
              下载完整的 SQLite 数据库文件作为备份
            </p>
          </div>
        </div>
      </div>

      <div class="border-t border-gray-200 px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">系统信息</h3>

        <dl class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
          <div>
            <dt class="text-sm font-medium text-gray-500">当前用户</dt>
            <dd class="mt-1 text-sm text-gray-900">
              {{ authStore.isAdmin ? '管理员' : '普通用户' }}
            </dd>
          </div>

          <div>
            <dt class="text-sm font-medium text-gray-500">权限说明</dt>
            <dd class="mt-1 text-sm text-gray-900">
              {{ authStore.isAdmin ? '可以添加、编辑、删除记录' : '仅可查看记录' }}
            </dd>
          </div>

          <div>
            <dt class="text-sm font-medium text-gray-500">版本</dt>
            <dd class="mt-1 text-sm text-gray-900">v1.0.0</dd>
          </div>

          <div>
            <dt class="text-sm font-medium text-gray-500">最后登录</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ new Date().toLocaleString() }}</dd>
          </div>
        </dl>
      </div>

      <div class="border-t border-gray-200 px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">帮助</h3>

        <div class="prose prose-sm text-gray-500">
          <p>NestEgg 是一个简单的家庭记账系统，帮助您轻松管理家庭财务。</p>
          <ul>
            <li>管理员可以添加、编辑和删除交易记录</li>
            <li>普通用户可以查看所有记录和统计信息</li>
            <li>支持按类型、分类、日期筛选记录</li>
            <li>提供月度和分类统计图表</li>
            <li>支持数据导出和备份</li>
          </ul>
        </div>
      </div>
    </div>

    <div v-if="message" class="mt-4 rounded-md p-4"
         :class="message.type === 'success' ? 'bg-green-50' : 'bg-red-50'">
      <p class="text-sm"
         :class="message.type === 'success' ? 'text-green-800' : 'text-red-800'">
        {{ message.text }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTransactionStore } from '@/stores/transaction'
import axios from 'axios'

const authStore = useAuthStore()
const transactionStore = useTransactionStore()

const message = ref(null)

async function exportCSV() {
  const result = await transactionStore.exportCSV()
  if (result.success) {
    showMessage('CSV 文件已下载', 'success')
  } else {
    showMessage(result.message, 'error')
  }
}

async function exportDatabase() {
  try {
    const response = await axios.get('/api/export/database', {
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `nestegg_backup_${new Date().toISOString().split('T')[0]}.db`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    showMessage('数据库备份已下载', 'success')
  } catch (error) {
    showMessage('备份失败', 'error')
  }
}

function showMessage(text, type) {
  message.value = { text, type }
  setTimeout(() => {
    message.value = null
  }, 3000)
}
</script>