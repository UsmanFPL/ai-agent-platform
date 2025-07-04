'use client'

import { useState, useEffect } from 'react'
import { CpuChipIcon, PlayIcon, PauseIcon, ClockIcon } from '@heroicons/react/24/outline'

interface Agent {
  id: string
  name: string
  type: string
  status: string
  created_at: string
  execution_count: number
  last_execution?: string
}

export default function AgentDashboard() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAgents()
  }, [])

  const fetchAgents = async () => {
    try {
      // Mock data since we don't have a full agents API yet
      setAgents([
        {
          id: '1',
          name: 'TAMS AI-Assist',
          type: 'automation',
          status: 'active',
          created_at: '2024-12-16T10:00:00Z',
          execution_count: 45,
          last_execution: '2024-12-16T14:30:00Z'
        },
        {
          id: '2', 
          name: 'Email Automation Agent',
          type: 'automation',
          status: 'idle',
          created_at: '2024-12-15T09:00:00Z',
          execution_count: 23,
          last_execution: '2024-12-16T12:15:00Z'
        },
        {
          id: '3',
          name: 'Document Processing Agent',
          type: 'assistive',
          status: 'idle',
          created_at: '2024-12-14T16:30:00Z',
          execution_count: 12,
          last_execution: '2024-12-16T11:45:00Z'
        }
      ])
    } catch (error) {
      console.error('Failed to fetch agents:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'idle':
        return 'bg-gray-100 text-gray-800'
      case 'error':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'automation':
        return <CpuChipIcon className="h-5 w-5 text-blue-600" />
      case 'assistive':
        return <PlayIcon className="h-5 w-5 text-purple-600" />
      default:
        return <CpuChipIcon className="h-5 w-5 text-gray-600" />
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString()
  }

  const testTAMSAgent = async () => {
    try {
      const response = await fetch('/api/v1/tams/test', {
        method: 'POST',
      })
      
      if (response.ok) {
        const result = await response.json()
        alert(`TAMS Test Successful!\nRisk Score: ${result.result?.final_recommendation?.overall_risk_score || 'N/A'}/10`)
        fetchAgents() // Refresh the list
      } else {
        alert('TAMS Test Failed')
      }
    } catch (error) {
      console.error('TAMS test error:', error)
      alert('TAMS Test Error')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Agent List */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Active Agents</h2>
        </div>
        
        <div className="divide-y divide-gray-200">
          {agents.map((agent) => (
            <div key={agent.id} className="px-6 py-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="flex-shrink-0 mr-4">
                    {getTypeIcon(agent.type)}
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-gray-900">{agent.name}</h3>
                    <p className="text-sm text-gray-500">Type: {agent.type}</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <p className="text-sm text-gray-900">{agent.execution_count} executions</p>
                    <p className="text-xs text-gray-500">
                      Last: {agent.last_execution ? formatDate(agent.last_execution) : 'Never'}
                    </p>
                  </div>
                  
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(agent.status)}`}>
                    {agent.status}
                  </span>
                  
                  {agent.name === 'TAMS AI-Assist' && (
                    <button
                      onClick={testTAMSAgent}
                      className="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded text-blue-700 bg-blue-100 hover:bg-blue-200"
                    >
                      <PlayIcon className="h-3 w-3 mr-1" />
                      Test
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button
            onClick={testTAMSAgent}
            className="flex items-center justify-center px-4 py-3 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            <PlayIcon className="h-4 w-4 mr-2" />
            Test TAMS Agent
          </button>
          
          <button className="flex items-center justify-center px-4 py-3 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
            <CpuChipIcon className="h-4 w-4 mr-2" />
            View All Agents
          </button>
          
          <button className="flex items-center justify-center px-4 py-3 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
            <ClockIcon className="h-4 w-4 mr-2" />
            Execution History
          </button>
        </div>
      </div>

      {/* System Status */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">System Status</h3>
        
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">API Server</span>
            <div className="flex items-center">
              <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
              <span className="text-sm text-green-600">Online</span>
            </div>
          </div>
          
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">LLM Provider</span>
            <div className="flex items-center">
              <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
              <span className="text-sm text-green-600">Connected</span>
            </div>
          </div>
          
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Database</span>
            <div className="flex items-center">
              <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
              <span className="text-sm text-green-600">Connected</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}