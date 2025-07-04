'use client'

import { useState } from 'react'
import { PlayIcon, ClockIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'

interface TAMSResult {
  status: string
  analysis: {
    stage1_genuine_correlation: any
    stage2_behavioral_analysis: any
    stage3_risk_assessment: any
  }
  final_recommendation: {
    final_classification: string
    overall_risk_score: number
    confidence_level: string
    next_actions: string[]
  }
  version: string
  execution_time_ms?: number
}

export default function TAMSAnalysis() {
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [result, setResult] = useState<TAMSResult | null>(null)
  const [formData, setFormData] = useState({
    timestamp: new Date().toISOString(),
    merchant: 'Unknown Online Store',
    amount: 299.99,
    transaction_type: 'Card-Not-Present',
    user_id: 'user_12345'
  })

  const handleAnalyze = async () => {
    setIsAnalyzing(true)
    setResult(null)

    try {
      const response = await fetch('/api/v1/tams/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        const data = await response.json()
        setResult(data)
      } else {
        console.error('Analysis failed:', response.statusText)
      }
    } catch (error) {
      console.error('Analysis error:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const getRiskColor = (score: number) => {
    if (score >= 7) return 'text-red-600 bg-red-100'
    if (score >= 4) return 'text-yellow-600 bg-yellow-100'
    return 'text-green-600 bg-green-100'
  }

  const getClassificationColor = (classification: string) => {
    if (classification.includes('High Priority')) return 'bg-red-100 text-red-800'
    if (classification.includes('Medium Priority')) return 'bg-yellow-100 text-yellow-800'
    return 'bg-green-100 text-green-800'
  }

  return (
    <div className="space-y-6">
      {/* Input Form */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Transaction Alert Analysis</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Merchant
            </label>
            <input
              type="text"
              value={formData.merchant}
              onChange={(e) => setFormData({ ...formData, merchant: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Amount ($)
            </label>
            <input
              type="number"
              value={formData.amount}
              onChange={(e) => setFormData({ ...formData, amount: parseFloat(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Transaction Type
            </label>
            <select
              value={formData.transaction_type}
              onChange={(e) => setFormData({ ...formData, transaction_type: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="Card-Not-Present">Card-Not-Present</option>
              <option value="Card-Present">Card-Present</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              User ID
            </label>
            <input
              type="text"
              value={formData.user_id}
              onChange={(e) => setFormData({ ...formData, user_id: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <button
          onClick={handleAnalyze}
          disabled={isAnalyzing}
          className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isAnalyzing ? (
            <>
              <ClockIcon className="h-4 w-4 mr-2 animate-spin" />
              Analyzing...
            </>
          ) : (
            <>
              <PlayIcon className="h-4 w-4 mr-2" />
              Run TAMS Analysis
            </>
          )}
        </button>
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {/* Final Recommendation */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Final Recommendation</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="text-center">
                <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getClassificationColor(result.final_recommendation.final_classification)}`}>
                  {result.final_recommendation.final_classification}
                </div>
              </div>
              
              <div className="text-center">
                <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full text-2xl font-bold ${getRiskColor(result.final_recommendation.overall_risk_score)}`}>
                  {result.final_recommendation.overall_risk_score}
                </div>
                <p className="text-sm text-gray-500 mt-1">Risk Score</p>
              </div>
              
              <div className="text-center">
                <div className="text-lg font-semibold text-gray-900">
                  {result.final_recommendation.confidence_level}
                </div>
                <p className="text-sm text-gray-500">Confidence</p>
              </div>
            </div>

            <div>
              <h4 className="font-medium text-gray-900 mb-2">Recommended Actions:</h4>
              <ul className="space-y-1">
                {result.final_recommendation.next_actions.map((action, index) => (
                  <li key={index} className="flex items-start">
                    <span className="flex-shrink-0 w-5 h-5 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-medium mr-2 mt-0.5">
                      {index + 1}
                    </span>
                    <span className="text-sm text-gray-700">{action}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Stage Analysis */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Stage 1 */}
            <div className="bg-white rounded-lg shadow p-6">
              <h4 className="font-semibold text-gray-900 mb-3">Stage 1: Genuine Correlation</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">Classification:</span>
                  <span className="text-sm font-medium">{result.analysis.stage1_genuine_correlation?.classification || 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">Confidence:</span>
                  <span className="text-sm font-medium">{result.analysis.stage1_genuine_correlation?.confidenceScore || 'N/A'}</span>
                </div>
              </div>
              {result.analysis.stage1_genuine_correlation?.htmlContent && (
                <div 
                  className="mt-4 text-xs"
                  dangerouslySetInnerHTML={{ __html: result.analysis.stage1_genuine_correlation.htmlContent }}
                />
              )}
            </div>

            {/* Stage 2 */}
            <div className="bg-white rounded-lg shadow p-6">
              <h4 className="font-semibold text-gray-900 mb-3">Stage 2: Behavioral Analysis</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">Anomaly Rating:</span>
                  <span className={`text-sm font-medium ${
                    result.analysis.stage2_behavioral_analysis?.anomalyRating === 'High' ? 'text-red-600' :
                    result.analysis.stage2_behavioral_analysis?.anomalyRating === 'Medium' ? 'text-yellow-600' : 'text-green-600'
                  }`}>
                    {result.analysis.stage2_behavioral_analysis?.anomalyRating || 'N/A'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">Observations:</span>
                  <span className="text-sm font-medium">{result.analysis.stage2_behavioral_analysis?.keyAnomalousObservations?.length || 0}</span>
                </div>
              </div>
              {result.analysis.stage2_behavioral_analysis?.htmlContent && (
                <div 
                  className="mt-4 text-xs"
                  dangerouslySetInnerHTML={{ __html: result.analysis.stage2_behavioral_analysis.htmlContent }}
                />
              )}
            </div>

            {/* Stage 3 */}
            <div className="bg-white rounded-lg shadow p-6">
              <h4 className="font-semibold text-gray-900 mb-3">Stage 3: Risk Assessment</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">Risk Rating:</span>
                  <span className={`text-sm font-medium ${getRiskColor(result.analysis.stage3_risk_assessment?.riskRating || 0).split(' ')[0]}`}>
                    {result.analysis.stage3_risk_assessment?.riskRating || 'N/A'}/10
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">Key Findings:</span>
                  <span className="text-sm font-medium">{result.analysis.stage3_risk_assessment?.keyFindings?.length || 0}</span>
                </div>
              </div>
              {result.analysis.stage3_risk_assessment?.htmlContent && (
                <div 
                  className="mt-4 text-xs"
                  dangerouslySetInnerHTML={{ __html: result.analysis.stage3_risk_assessment.htmlContent }}
                />
              )}
            </div>
          </div>

          {/* Performance Info */}
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center justify-between text-sm text-gray-600">
              <span>Analysis completed in {((result.execution_time_ms || 0) / 1000).toFixed(2)}s</span>
              <span>Version: {result.version}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}