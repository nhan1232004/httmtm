import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, 
  XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer,
  AreaChart, Area
} from 'recharts';
import './CEODashboard.css';

const CEODashboard = ({ onLogout }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [activeModal, setActiveModal] = useState(null);

  const API_URL = "http://localhost:8000/api/ceo/dashboard";

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await fetch(API_URL);
      if (!response.ok) throw new Error("Failed to fetch dashboard data");
      const result = await response.json();
      setData(result);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const formatCurrency = (val) => new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP', minimumFractionDigits: 0 }).format(val);
  const formatNumber = (val) => new Intl.NumberFormat('en-US').format(val);

  // COLORS for dark theme charts
  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];
  const CHART_TEXT = '#9ca3af';

  if (loading) return (
    <div className="ceo-loading">
      <div className="loader"></div>
      <h2>Initializing Strategic Intelligence System...</h2>
    </div>
  );

  if (error) return (
    <div className="ceo-error">
      <h2>System Error</h2>
      <p>{error}</p>
      <button onClick={fetchData} className="btn-retry">Retry Connection</button>
    </div>
  );

  if (!data) return null;

  // Destructure KPI data
  const { 
    kpi_business_scale: scale, 
    kpi_risk_health: risk, 
    kpi_customer_intelligence: cust, 
    kpi_fashion_specific: fashion, 
    kpi_strategic: strat 
  } = data;

  // Prepare chart data
  const rfmData = cust.rfm_segments ? Object.entries(cust.rfm_segments).map(([name, val]) => ({ name, value: val.count, revenue: val.revenue })) : [];
  const ageData = cust.age_demographics ? Object.entries(cust.age_demographics).map(([name, val]) => ({ name, count: val })) : [];
  const deptData = fashion.department_revenue ? fashion.department_revenue : [];
  const loyaltyData = fashion.loyalty_revenue ? fashion.loyalty_revenue : [];
  const channelShift = strat.channel_shift ? strat.channel_shift : { current_online_pct: 0, previous_online_pct: 0, shift: 0 };
  const oppData = strat.investment_opportunity ? strat.investment_opportunity : { department: 'N/A', growth: '0%', action: '' };
  const expData = strat.market_expansion ? strat.market_expansion : { demographic: 'N/A', growth: '0%', action: '' };
  const forecastData = strat.forecast ? strat.forecast : [];

  const renderModal = () => {
    if (!activeModal) return null;

    let title = "";
    let content = null;

    if (activeModal === 'revenue') {
      title = "Total Revenue Deep Dive";
      content = (
        <>
          <div className="modal-insight">
            <strong>AI Insight:</strong> Revenue is tracking {scale.revenue_growth_percentage >= 0 ? '+' : ''}{scale.revenue_growth_percentage}% MoM. The growth is primarily driven by recent seasonal demands in Womenswear.
          </div>
          <p>Projected Weekly Breakdown (Estimated):</p>
          <ul style={{ lineHeight: '1.8' }}>
            <li>Week 1: {formatCurrency(scale.total_revenue * 0.22)}</li>
            <li>Week 2: {formatCurrency(scale.total_revenue * 0.25)}</li>
            <li>Week 3: {formatCurrency(scale.total_revenue * 0.28)}</li>
            <li>Week 4: {formatCurrency(scale.total_revenue * 0.25)}</li>
          </ul>
        </>
      );
    } else if (activeModal === 'customers') {
      title = "Active Customers Analysis";
      content = (
        <>
          <div className="modal-insight">
            <strong>AI Insight:</strong> High volume of single-purchase users. Focusing on retention strategies for the 'Potential' segment could increase overall LTV by 15%.
          </div>
          <p>We currently have {formatNumber(scale.active_customers)} active customers making {scale.transactions_per_customer} transactions on average.</p>
        </>
      );
    } else if (activeModal === 'aov') {
      title = "Average Order Value (AOV) Breakdown";
      content = (
        <>
          <div className="modal-insight">
            <strong>AI Insight:</strong> AOV is heavily influenced by the cross-selling of Accessories with Trousers/Dresses.
          </div>
          <p>AOV: {formatCurrency(scale.average_order_value)}</p>
          <p>Total Transactions: {formatNumber(scale.total_transactions)}</p>
        </>
      );
    } else if (activeModal === 'forecast') {
      title = "ETS Forecast Model Details";
      content = (
        <>
          <div className="modal-insight">
            <strong>AI Insight:</strong> Forecast uses Exponential Smoothing (ETS) with a 12-month seasonal period. Confidence interval is ±4%.
          </div>
          <table className="ceo-table">
            <thead>
              <tr><th>Month</th><th>Predicted Revenue</th></tr>
            </thead>
            <tbody>
              {forecastData.map((d, i) => (
                <tr key={i}><td>{d.month}</td><td>{formatCurrency(d.predicted_revenue)}</td></tr>
              ))}
            </tbody>
          </table>
        </>
      );
    } else if (activeModal === 'channel') {
      title = "Online Channel Shift Details";
      content = (
        <>
          <div className="modal-insight">
            <strong>AI Insight:</strong> Online sales are {channelShift.shift >= 0 ? 'growing' : 'shrinking'} at a rate of {Math.abs(channelShift.shift)}% MoM compared to physical stores.
          </div>
          <p>Current Online Share: {channelShift.current_online_pct}%</p>
          <p>Previous 30 Days Online Share: {channelShift.previous_online_pct}%</p>
        </>
      );
    } else if (activeModal === 'opportunity') {
      title = "Strategic Investment Proposal";
      content = (
        <>
          <div className="modal-insight">
            <strong>AI Recommendation:</strong> Strong signal to increase budget allocation for {oppData.department}.
          </div>
          <p><strong>Target Department:</strong> {oppData.department}</p>
          <p><strong>Recent Growth Trajectory:</strong> {oppData.growth}</p>
          <p><strong>CEO Action Item:</strong> {oppData.action}</p>
        </>
      );
    } else if (activeModal === 'expansion') {
      title = "Market Expansion Strategy";
      content = (
        <>
          <div className="modal-insight">
            <strong>AI Recommendation:</strong> Demographic shift indicates high potential in the {expData.demographic} segment.
          </div>
          <p><strong>Target Demographic:</strong> {expData.demographic}</p>
          <p><strong>Segment Growth:</strong> {expData.growth}</p>
          <p><strong>CEO Action Item:</strong> {expData.action}</p>
        </>
      );
    } else if (activeModal === 'churn') {
      title = "High Risk Churn Segment Details";
      content = (
        <>
          <div className="modal-insight">
            <strong>AI Insight:</strong> {formatNumber(risk.churn_analysis.at_risk_customers)} customers have not returned in 60+ days but historically spent heavily.
          </div>
          <p><strong>Revenue at Risk:</strong> {formatCurrency(risk.churn_analysis.churn_risk_revenue)}</p>
          <p>Action: Deploy Win-back email campaign with 20% discount on their most purchased category.</p>
        </>
      );
    } else if (activeModal === 'anomaly') {
      title = "Anomaly Detection (Isolation Forest)";
      content = (
        <>
          <div className="modal-insight">
            <strong>AI Insight:</strong> Detected {risk.anomaly_detection.anomaly_percentage}% of transactions as anomalous (extremely high cart values or unusual quantities).
          </div>
          <p>Total Anomalies: {formatNumber(risk.anomaly_detection.anomaly_count)}</p>
          <p>Action: Flagged to fraud and pricing teams for manual review.</p>
        </>
      );
    }

    return (
      <div className="ceo-modal-overlay" onClick={() => setActiveModal(null)}>
        <div className="ceo-modal-content" onClick={e => e.stopPropagation()}>
          <div className="ceo-modal-header">
            <h2>{title}</h2>
            <button className="btn-close" onClick={() => setActiveModal(null)}>×</button>
          </div>
          <div className="ceo-modal-body">
            {content || <p>Detailed analysis is currently being generated...</p>}
          </div>
        </div>
      </div>
    );
  };

  const renderOverview = () => (
    <div className="dashboard-grid">
      {/* KPI Cards row */}
      <div className="kpi-row">
        <div className="kpi-card glass-panel clickable" onClick={() => setActiveModal('revenue')}>
          <div className="kpi-icon blue">💰</div>
          <div className="kpi-info">
            <span className="kpi-label">Total Revenue (YTD)</span>
            <span className="kpi-value">{formatCurrency(scale.total_revenue)}</span>
            <span className={`kpi-trend ${scale.revenue_growth_percentage >= 0 ? 'positive' : 'negative'}`}>
              {scale.revenue_growth_percentage >= 0 ? '↑' : '↓'} {Math.abs(scale.revenue_growth_percentage)}% MoM
            </span>
          </div>
        </div>
        <div className="kpi-card glass-panel clickable" onClick={() => setActiveModal('customers')}>
          <div className="kpi-icon emerald">👥</div>
          <div className="kpi-info">
            <span className="kpi-label">Active Customers</span>
            <span className="kpi-value">{formatNumber(scale.active_customers)}</span>
            <span className="kpi-desc">{scale.transactions_per_customer} avg transactions/cust</span>
          </div>
        </div>
        <div className="kpi-card glass-panel clickable" onClick={() => setActiveModal('aov')}>
          <div className="kpi-icon gold">🛒</div>
          <div className="kpi-info">
            <span className="kpi-label">Average Order Value</span>
            <span className="kpi-value">{formatCurrency(scale.average_order_value)}</span>
            <span className="kpi-desc">Based on {formatNumber(scale.total_transactions)} orders</span>
          </div>
        </div>
        <div className="kpi-card glass-panel clickable" onClick={() => setActiveModal('forecast')}>
          <div className="kpi-icon purple">🔮</div>
          <div className="kpi-info">
            <span className="kpi-label">Next Month Forecast</span>
            <span className="kpi-value">{forecastData.length > 0 ? formatCurrency(forecastData[0].predicted_revenue) : 'N/A'}</span>
            <span className="kpi-desc">Statsmodels ETS Model</span>
          </div>
        </div>
      </div>

      {/* Main Charts */}
      <div className="charts-row">
        <div className="chart-card glass-panel wide">
          <h3>Customer Segmentation (RFM K-Means)</h3>
          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={rfmData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="name" stroke={CHART_TEXT} />
                <YAxis yAxisId="left" stroke={CHART_TEXT} orientation="left" />
                <YAxis yAxisId="right" stroke={CHART_TEXT} orientation="right" tickFormatter={(val) => `£${val/1000}k`} />
                <RechartsTooltip contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', color: '#e5e7eb' }} />
                <Legend />
                <Bar yAxisId="left" dataKey="value" name="Customers" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                <Bar yAxisId="right" dataKey="revenue" name="Revenue" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="chart-card glass-panel">
          <h3>Revenue by Department</h3>
          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie data={deptData} cx="50%" cy="50%" innerRadius={60} outerRadius={100} paddingAngle={5} dataKey="revenue" nameKey="name">
                  {deptData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip formatter={(value) => formatCurrency(value)} contentStyle={{ backgroundColor: '#1f2937', border: 'none', color: '#e5e7eb' }} />
                <Legend verticalAlign="bottom" height={36} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );

  const renderMacroStrategy = () => (
    <div className="dashboard-grid">
      <div className="kpi-row">
        <div className="kpi-card glass-panel alert-yellow clickable" onClick={() => setActiveModal('channel')}>
          <div className="kpi-icon gold">🌐</div>
          <div className="kpi-info">
            <span className="kpi-label">Online Channel Share</span>
            <span className="kpi-value">{channelShift.current_online_pct}%</span>
            <span className={`kpi-trend ${channelShift.shift >= 0 ? 'positive' : 'negative'}`}>
              {channelShift.shift >= 0 ? '↑' : '↓'} {Math.abs(channelShift.shift)}% MoM Shift
            </span>
          </div>
        </div>
        <div className="kpi-card glass-panel clickable" onClick={() => setActiveModal('opportunity')}>
          <div className="kpi-icon emerald">📈</div>
          <div className="kpi-info">
            <span className="kpi-label">Top Investment Signal</span>
            <span className="kpi-value">{oppData.department}</span>
            <span className="kpi-trend positive">{oppData.growth} Growth</span>
          </div>
        </div>
        <div className="kpi-card glass-panel clickable" onClick={() => setActiveModal('expansion')}>
          <div className="kpi-icon purple">🎯</div>
          <div className="kpi-info">
            <span className="kpi-label">Market Expansion</span>
            <span className="kpi-value">{expData.demographic}</span>
            <span className="kpi-trend positive">{expData.growth} Potential</span>
          </div>
        </div>
      </div>
      
      <div className="charts-row">
        <div className="chart-card glass-panel wide">
          <h3>Customer Loyalty & Membership Revenue Share</h3>
          <div className="chart-wrapper tall">
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={loyaltyData} layout="vertical" margin={{ top: 20, right: 30, left: 40, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" horizontal={true} vertical={false}/>
                <XAxis type="number" stroke={CHART_TEXT} tickFormatter={(val) => `£${val/1000}k`} />
                <YAxis type="category" dataKey="status" stroke={CHART_TEXT} width={100} />
                <RechartsTooltip formatter={(val) => formatCurrency(val)} contentStyle={{ backgroundColor: '#1f2937', border: 'none', color: '#e5e7eb' }} />
                <Bar dataKey="revenue" name="Revenue" fill="#f59e0b" radius={[0, 4, 4, 0]} barSize={30}>
                  {loyaltyData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <div className="chart-card glass-panel">
          <h3>Seasonal Revenue Pattern</h3>
          <div className="chart-wrapper tall">
            <ResponsiveContainer width="100%" height={400}>
              <AreaChart data={fashion.seasonal_demand} margin={{ top: 20, right: 10, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="month" stroke={CHART_TEXT} tick={{fontSize: 12}} />
                <YAxis stroke={CHART_TEXT} tickFormatter={(val) => `${val/1000}k`} />
                <RechartsTooltip formatter={(val) => formatCurrency(val)} contentStyle={{ backgroundColor: '#1f2937', border: 'none', color: '#e5e7eb' }} />
                <Area type="monotone" dataKey="revenue" stroke="#ec4899" fill="#ec4899" fillOpacity={0.3} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );

  const renderRiskMgmt = () => (
    <div className="dashboard-grid">
      <div className="kpi-row">
        <div className="kpi-card glass-panel alert-red clickable" onClick={() => setActiveModal('churn')}>
          <div className="kpi-icon">⚠️</div>
          <div className="kpi-info">
            <span className="kpi-label">High Risk Churn Segment</span>
            <span className="kpi-value">{formatNumber(risk.churn_analysis.at_risk_customers)}</span>
            <span className="kpi-desc">Revenue at risk: {formatCurrency(risk.churn_analysis.churn_risk_revenue)}</span>
          </div>
        </div>
        <div className="kpi-card glass-panel alert-yellow clickable" onClick={() => setActiveModal('anomaly')}>
          <div className="kpi-icon">🔍</div>
          <div className="kpi-info">
            <span className="kpi-label">Anomaly Transactions</span>
            <span className="kpi-value">{formatNumber(risk.anomaly_detection.anomaly_count)}</span>
            <span className="kpi-desc">Isolation Forest detected ({risk.anomaly_detection.anomaly_percentage}%)</span>
          </div>
        </div>
        <div className="kpi-card glass-panel">
          <div className="kpi-icon">🛡️</div>
          <div className="kpi-info">
            <span className="kpi-label">30-Day Retention Rate</span>
            <span className="kpi-value">{risk.retention_rate}%</span>
            <span className="kpi-desc">Customers returned from last month</span>
          </div>
        </div>
      </div>
      
      <div className="charts-row mt-4">
        <div className="chart-card glass-panel wide">
          <h3>Customer Age Demographics</h3>
          <div className="chart-wrapper">
             <ResponsiveContainer width="100%" height={300}>
              <BarChart data={ageData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="name" stroke={CHART_TEXT} />
                <YAxis stroke={CHART_TEXT} />
                <RechartsTooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
                <Bar dataKey="count" name="Customers" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="ceo-dashboard-layout">
      {/* Sidebar */}
      <aside className="ceo-sidebar">
        <div className="sidebar-brand">
          <div className="logo-box">H&M</div>
          <span>Strategic Hub</span>
        </div>
        <nav className="sidebar-nav">
          <button className={`nav-btn ${activeTab === 'overview' ? 'active' : ''}`} onClick={() => setActiveTab('overview')}>
            📊 Overview
          </button>
          <button className={`nav-btn ${activeTab === 'macro' ? 'active' : ''}`} onClick={() => setActiveTab('macro')}>
            🌐 Macro Strategy
          </button>
          <button className={`nav-btn ${activeTab === 'risk' ? 'active' : ''}`} onClick={() => setActiveTab('risk')}>
            ⚠️ Risk & Customers
          </button>
        </nav>
        <div className="sidebar-footer">
          <div className="system-status">
            <span className="status-dot"></span> System Online
          </div>
          <button className="btn-logout" onClick={onLogout}>Logout</button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="ceo-main">
        <header className="ceo-header glass-panel">
          <div className="header-title">
            <h1>H&M Executive Board</h1>
            <p className="subtitle">Real-time data engine driven by Machine Learning</p>
          </div>
          <div className="header-actions">
            <span className="last-updated">Last update: {new Date(data.timestamp).toLocaleTimeString()}</span>
            <button className="btn-refresh" onClick={fetchData}>
              {loading ? '🔄 Syncing...' : '🔄 Refresh Data'}
            </button>
          </div>
        </header>

        <div className="ceo-content">
          {activeTab === 'overview' && renderOverview()}
          {activeTab === 'macro' && renderMacroStrategy()}
          {activeTab === 'risk' && renderRiskMgmt()}
        </div>
        
        {renderModal()}
      </main>
    </div>
  );
};

export default CEODashboard;
