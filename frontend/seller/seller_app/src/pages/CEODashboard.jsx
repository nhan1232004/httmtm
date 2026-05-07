import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './CEODashboard.css';

const API_BASE = 'http://localhost:8000/api';

const CEODashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 60000); // Refresh every 60s
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/ceo/dashboard`);
      setDashboardData(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Failed to fetch dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !dashboardData) {
    return (
      <div className="dashboard-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Đang tính toán dữ liệu CEO Dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="error-box">
          <h3>⚠️ Lỗi</h3>
          <p>{error}</p>
          <button onClick={fetchDashboardData}>Thử lại</button>
        </div>
      </div>
    );
  }

  if (!dashboardData) return null;

  const kpi = dashboardData.kpi || {};

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div>
          <h1>📊 CEO Executive Dashboard</h1>
          <p className="subtitle">ShopVN Strategic Intelligence Platform — Real-time Analytics for Executive Decisions</p>
        </div>
        <div className="header-actions">
          <span className="last-updated">Cập nhật: {new Date().toLocaleTimeString('vi-VN')}</span>
          <button onClick={fetchDashboardData} className="refresh-btn">🔄 Làm mới</button>
        </div>
      </header>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📈 Tổng quan
        </button>
        <button 
          className={`tab ${activeTab === 'risks' ? 'active' : ''}`}
          onClick={() => setActiveTab('risks')}
        >
          ⚠️ Rủi ro
        </button>
        <button 
          className={`tab ${activeTab === 'segmentation' ? 'active' : ''}`}
          onClick={() => setActiveTab('segmentation')}
        >
          👥 Phân khúc
        </button>
        <button 
          className={`tab ${activeTab === 'forecast' ? 'active' : ''}`}
          onClick={() => setActiveTab('forecast')}
        >
          🔮 Dự báo
        </button>
        <button 
          className={`tab ${activeTab === 'opportunities' ? 'active' : ''}`}
          onClick={() => setActiveTab('opportunities')}
        >
          💡 Cơ hội
        </button>
      </div>

      <div className="content">
        {/* ① TIER 1: BUSINESS SCALE */}
        {activeTab === 'overview' && (
          <div className="tier tier-1">
            <h2 className="tier-title">① Quy mô & sức khỏe doanh nghiệp</h2>
            <div className="kpi-grid kpi-6">
              <KPICard
                label="TỔNG DOANH THU"
                value={`£${(kpi.total_revenue / 1000000).toFixed(1)}M`}
                trend={kpi.revenue_growth_percentage}
                unit="%"
              />
              <KPICard
                label="KHÁCH HÀNG HOẠT ĐỘNG"
                value={kpi.active_customers?.toLocaleString() || '0'}
                trend={null}
              />
              <KPICard
                label="GIÁ TRỊ ĐƠN TB (AOV)"
                value={`£${kpi.average_order_value?.toFixed(2)}`}
                trend={null}
              />
              <KPICard
                label="TỔNG GIAO DỊCH"
                value={kpi.total_transactions?.toLocaleString() || '0'}
                trend={null}
              />
              <KPICard
                label="DOANH THU TB/GIAO DỊCH"
                value={`£${(kpi.total_revenue / kpi.total_transactions)?.toFixed(2)}`}
                trend={null}
              />
              <KPICard
                label="TỶ LỆ GD/KH"
                value={`${(kpi.total_transactions / kpi.active_customers)?.toFixed(1)}`}
                unit="GD/KH"
              />
            </div>

            {/* Channel Analysis */}
            <div className="subsection">
              <h3>Phân tích theo kênh bán hàng</h3>
              <div className="channel-grid">
                {kpi.channel_analysis && Object.entries(kpi.channel_analysis).map(([channel, data]) => (
                  <div key={channel} className="channel-card">
                    <p className="channel-name">{channel}</p>
                    <p className="channel-revenue">£{data.revenue?.toLocaleString()}</p>
                    <p className="channel-stats">{data.transactions?.toLocaleString()} GD · {data.revenue_percentage?.toFixed(1)}% DT</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Top Products */}
            <div className="subsection">
              <h3>Top 10 sản phẩm bán chạy</h3>
              <table className="products-table">
                <thead>
                  <tr>
                    <th>STT</th>
                    <th>Mã SP</th>
                    <th>Doanh thu</th>
                    <th>Số lần bán</th>
                  </tr>
                </thead>
                <tbody>
                  {kpi.top_products && kpi.top_products.map((prod, idx) => (
                    <tr key={prod.product_id}>
                      <td>{idx + 1}</td>
                      <td>{prod.product_id}</td>
                      <td>£{prod.revenue?.toLocaleString()}</td>
                      <td>{prod.sales}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ② TIER 2: RISK METRICS */}
        {activeTab === 'risks' && (
          <div className="tier tier-2">
            <h2 className="tier-title">② Rủi ro & ưu tiên hành động</h2>
            
            <div className="risk-grid">
              <div className="risk-card risk-high">
                <h3>🚨 Churn Risk (Khách sắp rời bỏ)</h3>
                <div className="metric">
                  <span className="label">Khách hàng nguy cơ cao:</span>
                  <span className="value">{kpi.churn_analysis?.at_risk_customers?.toLocaleString()}</span>
                </div>
                <div className="metric">
                  <span className="label">Doanh thu có nguy cơ mất:</span>
                  <span className="value">£{kpi.churn_analysis?.churn_risk_revenue?.toLocaleString()}</span>
                </div>
                <div className="metric">
                  <span className="label">Tỷ lệ giữ chân:</span>
                  <span className="value">{kpi.churn_analysis?.retention_rate?.toFixed(1)}%</span>
                </div>
                <p className="action">→ Hành động: Triển khai voucher giữ chân, loyalty program</p>
              </div>

              <div className="risk-card risk-medium">
                <h3>⚠️ Giao dịch bất thường</h3>
                <div className="metric">
                  <span className="label">Số lượng:</span>
                  <span className="value">{kpi.anomaly_detection?.anomaly_count}</span>
                </div>
                <div className="metric">
                  <span className="label">Doanh thu:</span>
                  <span className="value">£{kpi.anomaly_detection?.anomaly_revenue?.toLocaleString()}</span>
                </div>
                <div className="metric">
                  <span className="label">% Tổng GD:</span>
                  <span className="value">{kpi.anomaly_detection?.anomaly_percentage?.toFixed(2)}%</span>
                </div>
                <p className="action">→ Hành động: Review thủ công top giao dịch nghi vấn</p>
              </div>

              <div className="risk-card risk-info">
                <h3>ℹ️ Tỷ lệ hủy đơn</h3>
                <div className="metric">
                  <span className="label">Tỷ lệ:</span>
                  <span className="value">{kpi.cancel_rate?.cancel_rate?.toFixed(2)}%</span>
                </div>
                <div className="metric">
                  <span className="label">Số đơn ước tính:</span>
                  <span className="value">{kpi.cancel_rate?.estimated_cancels?.toLocaleString()}</span>
                </div>
                <p className="action">→ Hành động: Cải thiện UX checkout, tối ưu hóa giá shipping</p>
              </div>
            </div>
          </div>
        )}

        {/* ③ TIER 3: SEGMENTATION */}
        {activeTab === 'segmentation' && (
          <div className="tier tier-3">
            <h2 className="tier-title">③ Phân khúc khách hàng (RFM K-Means)</h2>
            <p className="subtitle">80/20 Rule: 20% KH → 78% doanh thu</p>
            
            <div className="segment-grid">
              {kpi.customer_segments && Object.entries(kpi.customer_segments).map(([segment, data]) => (
                <div key={segment} className={`segment-card segment-${segment.toLowerCase()}`}>
                  <h3>{segment}</h3>
                  <div className="segment-stats">
                    <div className="stat">
                      <span className="label">Số lượng KH:</span>
                      <span className="value">{data.customer_count?.toLocaleString()}</span>
                    </div>
                    <div className="stat">
                      <span className="label">Doanh thu:</span>
                      <span className="value">£{data.revenue?.toLocaleString()}</span>
                    </div>
                    <div className="stat">
                      <span className="label">% Doanh thu:</span>
                      <span className="value">{data.revenue_percentage?.toFixed(1)}%</span>
                    </div>
                  </div>
                  <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${data.revenue_percentage}%` }}></div>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="strategy-box">
              <h3>💡 Chiến lược</h3>
              <ul>
                <li><strong>Champions:</strong> Tăng LTV: VIP program, early access sản phẩm mới</li>
                <li><strong>Loyal:</strong> Chuyển sang Champions: Cross-sell, bundle deals</li>
                <li><strong>Potential:</strong> Kích hoạt: Personalized recommendations</li>
                <li><strong>At-Risk:</strong> Giữ chân: Discount, special offers</li>
                <li><strong>Lost:</strong> Tái kích hoạt: Win-back campaigns</li>
              </ul>
            </div>
          </div>
        )}

        {/* ④ TIER 4: FORECAST */}
        {activeTab === 'forecast' && (
          <div className="tier tier-4">
            <h2 className="tier-title">④ Dự báo doanh thu 3 tháng (Prophet)</h2>
            
            <div className="forecast-grid">
              {kpi.revenue_forecast?.forecasts && kpi.revenue_forecast.forecasts.map((forecast, idx) => (
                <div key={idx} className={`forecast-card ${forecast.growth_percentage >= 0 ? 'positive' : 'negative'}`}>
                  <p className="month">{forecast.month}</p>
                  <p className="revenue">£{forecast.predicted_revenue?.toLocaleString()}</p>
                  <p className="growth">
                    {forecast.growth_percentage >= 0 ? '↑' : '↓'} {Math.abs(forecast.growth_percentage)?.toFixed(1)}%
                  </p>
                </div>
              ))}
            </div>

            <div className="forecast-actions">
              <h3>📋 Các bước chuẩn bị</h3>
              <ul>
                <li>📦 Tăng tồn kho 20% cho top 10 SKU</li>
                <li>📢 Chuẩn bị marketing campaign và flash sale</li>
                <li>📞 Tăng nhân lực support 30%</li>
                <li>🚚 Tối ưu hóa logistics, chuẩn bị kho trung chuyển</li>
              </ul>
            </div>
          </div>
        )}

        {/* ⑤ TIER 5: OPPORTUNITIES */}
        {activeTab === 'opportunities' && (
          <div className="tier tier-5">
            <h2 className="tier-title">⑤ Cơ hội kinh doanh (FP-Growth)</h2>
            <p className="subtitle">Top bundle recommendations — Lift cao nhất</p>
            
            {kpi.cross_sell_opportunities?.opportunities && kpi.cross_sell_opportunities.opportunities.length > 0 ? (
              <div className="opportunities-list">
                {kpi.cross_sell_opportunities.opportunities.map((opp, idx) => (
                  <div key={idx} className="opportunity-card">
                    <div className="opportunity-info">
                      <h4>{opp.product_pair}</h4>
                      <p>Confidence: {(opp.confidence * 100).toFixed(1)}%</p>
                    </div>
                    <div className="opportunity-metrics">
                      <span className="badge badge-lift">Lift {opp.lift}×</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-data">Chưa đủ dữ liệu để tính toán</p>
            )}

            <div className="implementation">
              <h3>🚀 Triển khai</h3>
              <ul>
                <li>Thêm "Frequently bought together" section trên product page</li>
                <li>Tạo bundle packages với discount 10-15%</li>
                <li>Automated email recommendations đến existing customers</li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// ──────────────────────────────────────
//  KPI Card Component
// ──────────────────────────────────────

const KPICard = ({ label, value, trend, unit = '' }) => {
  const trendClass = trend > 0 ? 'up' : trend < 0 ? 'down' : '';
  const trendIcon = trend > 0 ? '↑' : trend < 0 ? '↓' : '';

  return (
    <div className={`kpi-card ${trendClass}`}>
      <p className="kpi-label">{label}</p>
      <p className="kpi-value">{value}</p>
      {trend !== null && trend !== undefined && (
        <p className={`kpi-trend ${trendClass}`}>
          {trendIcon} {Math.abs(trend).toFixed(1)}{unit}
        </p>
      )}
    </div>
  );
};

export default CEODashboard;
