"""
Hệ thống Điều phối Chính (Master Pipeline Orchestrator)
Kết nối liền mạch toàn bộ 6 bước từ nhận ý định đến phản hồi điều hành
"""

import uuid
from typing import Dict, Any

from core.step1_intent_parser import IntentContextParser
from core.step2_secure_sql import SecureQueryEngine
from core.step3_data_quarantine import DataProfilerQuarantine
from core.step4_root_cause import DeepAnalyticsEngine
from core.step5_viz_summary import VisualizationSummaryEngine
from core.step6_delivery_feedback import DeliveryFeedbackEngine

class EnterpriseAnalyticsAgent:
    def __init__(self):
        self.step1_parser = IntentContextParser()
        self.step2_query = SecureQueryEngine()
        self.step3_profiler = DataProfilerQuarantine()
        self.step4_analytics = DeepAnalyticsEngine()
        self.step5_summary = VisualizationSummaryEngine()
        self.step6_delivery = DeliveryFeedbackEngine()

    def run(self, user_query: str, user_role: str = "CEO", as_of_date: str = "2026-11-16") -> Dict[str, Any]:
        """
        Thực thi quy trình 6 bước chuẩn BA Data Analytics Agent
        """
        conversation_id = str(uuid.uuid4())[:8]
        pipeline_log = []

        # ==========================================
        # BƯỚC 1: TIẾP NHẬN & HIỂU Ý ĐỊNH
        # ==========================================
        pipeline_log.append("▶ [BƯỚC 1] Bóc tách thực thể và ánh xạ Semantic Layer...")
        parsed_context = self.step1_parser.parse(user_query, user_role, as_of_date)

        # ==========================================
        # BƯỚC 2: LẬP KẾ HOẠCH & TRUY VẤN AN TOÀN
        # ==========================================
        pipeline_log.append("▶ [BƯỚC 2] Lập kế hoạch truy vấn, kiểm duyệt AST Guardrails và PII Masking...")
        plan_queries = self.step2_query.generate_plan_queries(parsed_context)
        
        # Thực thi lấy dữ liệu bán hàng
        df_raw_sales, sales_exec_logs = self.step2_query.execute_with_retry(
            plan_queries["sales_transactions"], user_role=user_role
        )
        pipeline_log.extend(sales_exec_logs)

        # Thực thi lấy dữ liệu ngoại cảnh (Thời tiết & Foot Traffic)
        df_external, ext_exec_logs = self.step2_query.execute_with_retry(
            plan_queries["traffic_weather"], user_role=user_role
        )

        # ==========================================
        # BƯỚC 3: LÀM SẠCH & KIỂM ĐỊNH CHẤT LƯỢNG
        # ==========================================
        pipeline_log.append("▶ [BƯỚC 3] Kiểm định chất lượng dữ liệu trong Sandbox và cách ly dữ liệu lỗi...")
        df_clean, df_quarantine, dq_metrics = self.step3_profiler.profile_and_quarantine(df_raw_sales)
        pipeline_log.append(f"   -> Kết quả: {dq_metrics['clean_records']:,} dòng sạch, {dq_metrics['dirty_records']} dòng cách ly. Điểm chất lượng: {dq_metrics['quality_score']}%")

        # ==========================================
        # BƯỚC 4: PHÂN TÍCH CHUYÊN SÂU & TÌM GỐC RỄ
        # ==========================================
        pipeline_log.append("▶ [BƯỚC 4] Chạy mô hình phân tích đóng góp, tương quan Pearson và Pareto...")
        analytics_results = self.step4_analytics.analyze(df_clean, df_external, parsed_context)

        # ==========================================
        # BƯỚC 5: TRỰC QUAN HÓA & TỔNG HỢP INSIGHT
        # ==========================================
        pipeline_log.append("▶ [BƯỚC 5] Khởi tạo biểu đồ tương tác Plotly và lập Executive Summary...")
        chart_waterfall = self.step5_summary.build_waterfall_chart(
            analytics_results["kpi_summary"],
            analytics_results["store_breakdown"]
        )
        chart_pareto = self.step5_summary.build_pareto_chart(
            analytics_results["pareto_stores"]
        )
        chart_forecast = self.step5_summary.build_forecast_chart(
            df_clean,
            analytics_results["short_term_forecast"]
        )
        executive_summary = self.step5_summary.generate_executive_summary(
            analytics_results, dq_metrics, parsed_context
        )

        # ==========================================
        # BƯỚC 6: PHẢN HỒI & CẢNH BÁO CHỦ ĐỘNG
        # ==========================================
        pipeline_log.append("▶ [BƯỚC 6] Đánh giá ngưỡng cảnh báo rủi ro và đóng gói báo cáo...")
        active_alerts = self.step6_delivery.evaluate_proactive_alerts(analytics_results, dq_metrics)
        excel_bytes = self.step6_delivery.export_to_excel(df_clean, df_quarantine)

        return {
            "conversation_id": conversation_id,
            "pipeline_log": pipeline_log,
            "step1_parsed_context": parsed_context,
            "step2_queries": plan_queries,
            "step2_raw_count": len(df_raw_sales),
            "step3_clean_df": df_clean,
            "step3_quarantine_df": df_quarantine,
            "step3_dq_metrics": dq_metrics,
            "step4_analytics": analytics_results,
            "step5_waterfall": chart_waterfall,
            "step5_pareto": chart_pareto,
            "step5_forecast": chart_forecast,
            "step5_executive_summary": executive_summary,
            "step6_alerts": active_alerts,
            "step6_excel_bytes": excel_bytes
        }

