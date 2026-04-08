"""
Test Suite for Visualization System v4.0

High Standard: 100% test pass rate
Tests all components with comprehensive coverage:
- ChartEngine (8 chart types)
- Dashboard (widgets, layout)
- ReportGenerator (3 formats)
- Visualizer (integration)
"""

import sys
from datetime import datetime

from visualization import (
    Visualizer,
    ChartEngine,
    Dashboard,
    ReportGenerator,
    Chart,
    ChartConfig,
    DataSeries,
    Widget,
    ChartType,
    ExportFormat,
    create_visualizer,
    create_performance_dashboard,
    create_quick_chart,
)


def test_data_series():
    """Test DataSeries data class"""
    print("Testing DataSeries...")
    
    series = DataSeries(
        name="Test Series",
        data=[1, 2, 3, 4, 5],
        color="#5470c6",
        labels=["A", "B", "C", "D", "E"],
    )
    
    # Test serialization
    data = series.to_dict()
    assert data["name"] == "Test Series"
    assert data["data"] == [1, 2, 3, 4, 5]
    
    # Test deserialization
    restored = DataSeries.from_dict(data)
    assert restored.name == series.name
    assert restored.data == series.data
    
    print("  [OK] DataSeries tests passed")
    return True


def test_chart_config():
    """Test ChartConfig data class"""
    print("Testing ChartConfig...")
    
    config = ChartConfig(
        title="Test Chart",
        chart_type=ChartType.LINE,
        x_label="X Axis",
        y_label="Y Axis",
        width=800,
        height=400,
    )
    
    # Test serialization
    data = config.to_dict()
    assert data["title"] == "Test Chart"
    assert data["chart_type"] == "LINE"
    
    # Test deserialization
    restored = ChartConfig.from_dict(data)
    assert restored.title == config.title
    assert restored.chart_type == config.chart_type
    
    print("  [OK] ChartConfig tests passed")
    return True


def test_chart_engine_line():
    """Test ChartEngine line chart"""
    print("Testing ChartEngine - Line Chart...")
    
    engine = ChartEngine()
    series = [
        DataSeries(name="Series 1", data=[1, 2, 3, 4, 5]),
        DataSeries(name="Series 2", data=[2, 4, 6, 8, 10]),
    ]
    
    chart = engine.create_line_chart(
        title="Line Chart Test",
        series=series,
        x_label="X",
        y_label="Y",
    )
    
    assert chart.config.chart_type == ChartType.LINE
    assert chart.config.title == "Line Chart Test"
    assert len(chart.series) == 2
    assert chart.id in engine.charts
    
    print("  [OK] Line chart tests passed")
    return True


def test_chart_engine_bar():
    """Test ChartEngine bar chart"""
    print("Testing ChartEngine - Bar Chart...")
    
    engine = ChartEngine()
    series = [DataSeries(name="Values", data=[10, 20, 30, 40])]
    
    chart = engine.create_bar_chart(
        title="Bar Chart Test",
        series=series,
    )
    
    assert chart.config.chart_type == ChartType.BAR
    assert len(chart.series) == 1
    
    print("  [OK] Bar chart tests passed")
    return True


def test_chart_engine_pie():
    """Test ChartEngine pie chart"""
    print("Testing ChartEngine - Pie Chart...")
    
    engine = ChartEngine()
    data = [("A", 30), ("B", 40), ("C", 30)]
    
    chart = engine.create_pie_chart(
        title="Pie Chart Test",
        data=data,
    )
    
    assert chart.config.chart_type == ChartType.PIE
    assert len(chart.series) == 1
    assert chart.series[0].labels == ["A", "B", "C"]
    
    print("  [OK] Pie chart tests passed")
    return True


def test_chart_engine_scatter():
    """Test ChartEngine scatter plot"""
    print("Testing ChartEngine - Scatter Plot...")
    
    engine = ChartEngine()
    x_data = [1, 2, 3, 4, 5]
    y_data = [2, 4, 6, 8, 10]
    
    chart = engine.create_scatter_plot(
        title="Scatter Plot Test",
        x_data=x_data,
        y_data=y_data,
    )
    
    assert chart.config.chart_type == ChartType.SCATTER
    
    print("  [OK] Scatter plot tests passed")
    return True


def test_chart_engine_heatmap():
    """Test ChartEngine heatmap"""
    print("Testing ChartEngine - Heatmap...")
    
    engine = ChartEngine()
    data = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    
    chart = engine.create_heatmap(
        title="Heatmap Test",
        data=data,
    )
    
    assert chart.config.chart_type == ChartType.HEATMAP
    
    print("  [OK] Heatmap tests passed")
    return True


def test_chart_engine_radar():
    """Test ChartEngine radar chart"""
    print("Testing ChartEngine - Radar Chart...")
    
    engine = ChartEngine()
    indicators = ["Speed", "Quality", "Cost", "Time"]
    series = [DataSeries(name="Product A", data=[80, 90, 70, 85])]
    
    chart = engine.create_radar_chart(
        title="Radar Chart Test",
        indicators=indicators,
        series=series,
    )
    
    assert chart.config.chart_type == ChartType.RADAR
    
    print("  [OK] Radar chart tests passed")
    return True


def test_chart_engine_gauge():
    """Test ChartEngine gauge"""
    print("Testing ChartEngine - Gauge...")
    
    engine = ChartEngine()
    
    chart = engine.create_gauge(
        title="CPU Usage",
        value=75.5,
        min_val=0,
        max_val=100,
    )
    
    assert chart.config.chart_type == ChartType.GAUGE
    assert chart.series[0].data[0] == 75.5
    
    print("  [OK] Gauge tests passed")
    return True


def test_chart_update():
    """Test chart data update"""
    print("Testing Chart Data Update...")
    
    engine = ChartEngine()
    series = [DataSeries(name="Data", data=[1, 2, 3])]
    chart = engine.create_line_chart("Test", series)
    
    # Update data
    new_series = [DataSeries(name="Data", data=[4, 5, 6])]
    success = engine.update_chart_data(chart.id, new_series)
    
    assert success is True
    assert engine.get_chart(chart.id).series[0].data == [4, 5, 6]
    
    print("  [OK] Chart update tests passed")
    return True


def test_dashboard_creation():
    """Test Dashboard creation"""
    print("Testing Dashboard Creation...")
    
    dashboard = Dashboard("Test Dashboard")
    assert dashboard.title == "Test Dashboard"
    assert len(dashboard.widgets) == 0
    
    print("  [OK] Dashboard creation tests passed")
    return True


def test_dashboard_widgets():
    """Test Dashboard widgets"""
    print("Testing Dashboard Widgets...")
    
    dashboard = Dashboard("Test Dashboard")
    engine = ChartEngine()
    
    # Add chart widget
    chart = engine.create_line_chart("Chart", [DataSeries(name="Data", data=[1, 2, 3])])
    widget_id = dashboard.add_chart_widget("My Chart", chart)
    
    assert widget_id in dashboard.widgets
    assert dashboard.widgets[widget_id].chart == chart
    
    # Add metrics widget
    metrics = [
        {"label": "Metric 1", "value": "100"},
        {"label": "Metric 2", "value": "200"},
    ]
    metrics_id = dashboard.add_metrics_widget("Metrics", metrics)
    
    assert metrics_id in dashboard.widgets
    assert dashboard.widgets[metrics_id].metrics == metrics
    
    print("  [OK] Dashboard widgets tests passed")
    return True


def test_dashboard_layout():
    """Test Dashboard layout management"""
    print("Testing Dashboard Layout...")
    
    dashboard = Dashboard("Test Dashboard")
    engine = ChartEngine()
    chart = engine.create_line_chart("Chart", [DataSeries(name="Data", data=[1, 2, 3])])
    
    widget_id = dashboard.add_chart_widget(
        "My Chart",
        chart,
        position={"x": 0, "y": 0, "w": 6, "h": 4}
    )
    
    # Update position
    success = dashboard.update_widget_position(widget_id, x=1, y=2, w=8, h=6)
    assert success is True
    
    widget = dashboard.get_widget(widget_id)
    assert widget.position["x"] == 1
    assert widget.position["y"] == 2
    assert widget.position["w"] == 8
    assert widget.position["h"] == 6
    
    print("  [OK] Dashboard layout tests passed")
    return True


def test_dashboard_serialization():
    """Test Dashboard serialization"""
    print("Testing Dashboard Serialization...")
    
    dashboard = Dashboard("Test Dashboard")
    engine = ChartEngine()
    chart = engine.create_line_chart("Chart", [DataSeries(name="Data", data=[1, 2, 3])])
    dashboard.add_chart_widget("My Chart", chart)
    
    data = dashboard.to_dict()
    assert data["title"] == "Test Dashboard"
    assert data["widget_count"] == 1
    assert "widgets" in data
    assert "layout" in data
    
    print("  [OK] Dashboard serialization tests passed")
    return True


def test_report_generator():
    """Test ReportGenerator"""
    print("Testing ReportGenerator...")
    
    generator = ReportGenerator()
    
    # Test HTML generation
    data = {
        "title": "Test Report",
        "items": [1, 2, 3],
        "metrics": {"a": 1, "b": 2},
    }
    
    html = generator.generate_report(data, template="summary", format=ExportFormat.HTML)
    assert "<html>" in html.lower()
    assert "Test Report" in html
    
    # Test JSON generation
    json_str = generator.generate_report(data, template="summary", format=ExportFormat.JSON)
    assert "Test Report" in json_str
    
    # Test Markdown generation
    md = generator.generate_report(data, template="summary", format=ExportFormat.MARKDOWN)
    assert "# Test Report" in md
    
    print("  [OK] ReportGenerator tests passed")
    return True


def test_report_templates():
    """Test ReportGenerator templates"""
    print("Testing Report Templates...")
    
    generator = ReportGenerator()
    
    # Test summary template
    data = {"title": "Summary", "items": [1, 2, 3], "metrics": {"a": 1}}
    result = generator.generate_report(data, template="summary", format=ExportFormat.JSON)
    assert "summary" in result.lower()
    
    # Test detailed template
    data = {"title": "Detailed", "overview": "Overview text", "details": [1, 2, 3]}
    result = generator.generate_report(data, template="detailed", format=ExportFormat.JSON)
    assert "sections" in result.lower()
    
    # Test metrics template
    data = {"title": "Metrics", "metrics": {"cpu": 50, "memory": 80}}
    result = generator.generate_report(data, template="metrics", format=ExportFormat.JSON)
    assert "metrics" in result.lower()
    
    print("  [OK] Report templates tests passed")
    return True


def test_visualizer():
    """Test Visualizer integration"""
    print("Testing Visualizer...")
    
    viz = Visualizer()
    
    # Test dashboard creation
    dashboard = viz.create_dashboard("My Dashboard")
    assert dashboard.title == "My Dashboard"
    
    # Test performance dashboard
    metrics = {
        "cpu": [10, 20, 30, 40, 50],
        "memory": [50, 55, 60, 65, 70],
    }
    perf_dashboard = viz.create_performance_dashboard(metrics, "Performance")
    assert perf_dashboard.title == "Performance"
    assert len(perf_dashboard.widgets) > 0
    
    # Test comparison chart
    categories = ["A", "B", "C"]
    values = {"Group 1": [10, 20, 30], "Group 2": [15, 25, 35]}
    chart = viz.create_comparison_chart(categories, values, "Comparison")
    assert chart.config.chart_type == ChartType.BAR
    
    # Test distribution pie
    data = {"Category A": 40, "Category B": 60}
    pie = viz.create_distribution_pie(data, "Distribution")
    assert pie.config.chart_type == ChartType.PIE
    
    # Test summary
    summary = viz.get_summary()
    assert "dashboards" in summary
    assert "charts" in summary
    
    print("  [OK] Visualizer tests passed")
    return True


def test_visualizer_export():
    """Test Visualizer export functionality"""
    print("Testing Visualizer Export...")
    
    viz = Visualizer()
    dashboard = viz.create_dashboard("Export Test")
    
    # Export to JSON
    json_str = viz.export_dashboard(dashboard, format=ExportFormat.JSON)
    assert "Export Test" in json_str
    
    # Export to HTML
    html = viz.export_dashboard(dashboard, format=ExportFormat.HTML)
    assert "<html>" in html.lower()
    
    print("  [OK] Visualizer export tests passed")
    return True


def test_factory_functions():
    """Test factory functions"""
    print("Testing Factory Functions...")
    
    # Test create_visualizer
    viz = create_visualizer()
    assert isinstance(viz, Visualizer)
    
    # Test create_performance_dashboard
    metrics = {"cpu": [10, 20, 30], "memory": [40, 50, 60]}
    dashboard = create_performance_dashboard(metrics, "Perf")
    assert isinstance(dashboard, Dashboard)
    assert dashboard.title == "Perf"
    
    # Test create_quick_chart
    chart = create_quick_chart(ChartType.LINE, "Quick", [1, 2, 3])
    assert isinstance(chart, Chart)
    assert chart.config.chart_type == ChartType.LINE
    
    print("  [OK] Factory functions tests passed")
    return True


def test_chart_serialization():
    """Test Chart serialization"""
    print("Testing Chart Serialization...")
    
    engine = ChartEngine()
    series = [DataSeries(name="Data", data=[1, 2, 3])]
    chart = engine.create_line_chart("Test", series)
    
    # Serialize
    data = chart.to_dict()
    assert data["config"]["title"] == "Test"
    assert len(data["series"]) == 1
    
    # Deserialize
    restored = Chart.from_dict(data)
    assert restored.config.title == chart.config.title
    assert len(restored.series) == len(chart.series)
    
    print("  [OK] Chart serialization tests passed")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Visualization System v4.0 - Test Suite")
    print("High Standard: 100% Pass Rate")
    print("=" * 60)
    
    tests = [
        test_data_series,
        test_chart_config,
        test_chart_engine_line,
        test_chart_engine_bar,
        test_chart_engine_pie,
        test_chart_engine_scatter,
        test_chart_engine_heatmap,
        test_chart_engine_radar,
        test_chart_engine_gauge,
        test_chart_update,
        test_dashboard_creation,
        test_dashboard_widgets,
        test_dashboard_layout,
        test_dashboard_serialization,
        test_report_generator,
        test_report_templates,
        test_visualizer,
        test_visualizer_export,
        test_factory_functions,
        test_chart_serialization,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"  [FAILED] {test.__name__}")
        except Exception as e:
            failed += 1
            print(f"  [FAILED] {test.__name__}: {e}")
    
    print("=" * 60)
    print(f"Results: {passed}/{len(tests)} tests passed ({passed/len(tests)*100:.1f}%)")
    print("=" * 60)
    
    if failed == 0:
        print("[OK] ALL TESTS PASSED - High Standard Achieved!")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
