/**
 * 东盟基建工程与涉外法查明 Agent 真实业务 API 聚合模块
 * 完全直连后端 FastAPI 服务，已移除所有 Mock 数据
 * 对齐技术方案与前后端 REST & SSE 契约
 */

import { request, ApiError, downloadBlob } from './client';
import {
  CaseState,
  CaseSummary,
  CaseMeta,
  SearchFilter,
  NormOrCaseItem,
  MaterialVerificationResult,
  Expert,
  ConsultRecord,
  SearchTraceItem,
  UserRole,
  ReviewErrorType,
  AgentWorkflowResponse,
  CaseChatMessage,
  CaseChatResponse,
  SavedInsight,
  SaveInsightPayload,
  StrategicAssessment,
  IntakeExtractResponse,
  AttachedArtifact,
} from '../types/lawAgent';

export const lawAgentApi = {
  /**
   * 获取当前主体名下的案件列表
   * 对应 GET /cases
   */
  async getCases(role: UserRole = 'practitioner'): Promise<CaseSummary[]> {
    return await request<CaseSummary[]>('/cases', {
      method: 'GET',
      params: { role },
    });
  },

  /**
   * 获取单个案件详细状态
   * 对应 GET /cases/{id}
   */
  async getCase(caseId: string): Promise<CaseState> {
    return await request<CaseState>(`/cases/${caseId}`, {
      method: 'GET',
    });
  },

  /**
   * 获取案件动态胜败边界推演与红队攻防对抗评估 (方案 A)
   * 对应 GET /cases/{id}/strategic-assessment
   */
  async getStrategicAssessment(caseId: string): Promise<StrategicAssessment> {
    return await request<StrategicAssessment>(`/cases/${caseId}/strategic-assessment`, {
      method: 'GET',
    });
  },

  /**
   * 创建新案件 (S0录入)
   * 对应 POST /cases
   */
  async createCase(payload: {
    title: string;
    facts_zh: string;
    claims_zh?: string;
    meta: CaseMeta;
    materials?: Array<{ name: string; desc_zh: string; excerpt_zh?: string }>;
    consent_version: string;
  }): Promise<{ case_id: string; initial_state: CaseState }> {
    return await request<{ case_id: string; initial_state: CaseState }>('/cases', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  /**
   * 启动或恢复查明工作流
   * 对应 POST /cases/{id}/run
   */
  async runWorkflow(caseId: string): Promise<{ job_id: string }> {
    return await request<{ job_id: string }>(`/cases/${caseId}/run`, {
      method: 'POST',
    });
  },

  /**
   * 人工闸门确认 (CISG闸门、S3争点确认、S8人工审阅完成)
   * 对应 POST /cases/{id}/confirm/{gate}
   */
  async confirmGate(
    caseId: string,
    gate: 'cisg' | 's3' | 's8',
    payload: any
  ): Promise<{ ok: boolean; updated_state: CaseState }> {
    return await request<{ ok: boolean; updated_state: CaseState }>(
      `/cases/${caseId}/confirm/${gate}`,
      {
        method: 'POST',
        body: JSON.stringify(payload),
      }
    );
  },

  /**
   * 追加待查明问题 (Follow-up)
   * 对应 POST /cases/{id}/followup
   */
  async followupQuestion(caseId: string, questionText: string): Promise<CaseState> {
    return await request<CaseState>(`/cases/${caseId}/followup`, {
      method: 'POST',
      body: JSON.stringify({ question_text: questionText }),
    });
  },

  /**
   * 逐条审阅陈述（采纳、修改、拒绝）
   * 对应 PATCH /cases/{id}/statements/{sid}
   */
  async updateStatementReview(
    caseId: string,
    sid: string,
    action: 'accept' | 'edit' | 'reject',
    errorType?: ReviewErrorType,
    note?: string,
    updatedText?: string
  ): Promise<CaseState> {
    return await request<CaseState>(`/cases/${caseId}/statements/${sid}`, {
      method: 'PATCH',
      body: JSON.stringify({
        action,
        error_type: errorType,
        note,
        updated_text: updatedText,
      }),
    });
  },

  /**
   * 删除案件 (安全彻底删除)
   * 对应 DELETE /cases/{id}
   */
  async deleteCase(caseId: string): Promise<boolean> {
    await request<void>(`/cases/${caseId}`, { method: 'DELETE' });
    return true;
  },

  /**
   * 东盟工程法律条文与权威先例判决检索
   * 对应 GET /search
   */
  async searchNormsAndCases(query: string, filters?: SearchFilter): Promise<NormOrCaseItem[]> {
    return await request<NormOrCaseItem[]>('/search', {
      method: 'GET',
      params: {
        q: query,
        law: filters?.law,
        court: filters?.court,
        kind: filters?.kind,
      },
    });
  },

  /**
   * 当事人外国法材料核验与工程合同条款强行法红线扫描 (F16)
   * 对应 POST /verify-materials
   */
  async verifyForeignMaterials(
    text: string,
    mode: 'CITATION_CHECK' | 'CONTRACT_REDLINE_AUDIT' = 'CONTRACT_REDLINE_AUDIT'
  ): Promise<MaterialVerificationResult> {
    return await request<MaterialVerificationResult>('/verify-materials', {
      method: 'POST',
      body: JSON.stringify({ raw_text: text, mode }),
    });
  },

  /**
   * 专家名录 (F17)
   * 对应 GET /experts
   */
  async getExperts(): Promise<Expert[]> {
    return await request<Expert[]>('/experts', {
      method: 'GET',
    });
  },

  /**
   * 会商流转记录 (F17)
   * 对应 GET /consults
   */
  async getConsults(caseId?: string): Promise<ConsultRecord[]> {
    return await request<ConsultRecord[]>('/consults', {
      method: 'GET',
      params: { case_id: caseId },
    });
  },

  /**
   * 发起专家会商咨询
   * 对应 POST /consults
   */
  async createConsult(payload: {
    case_id: string;
    expert_id: string;
    question_snapshot: string;
    evidence_summary: string;
  }): Promise<ConsultRecord> {
    return await request<ConsultRecord>('/consults', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  /**
   * 检索轨迹查看 (可解释性)
   * 对应 GET /cases/{id}/traces
   */
  async getSearchTraces(caseId: string): Promise<SearchTraceItem[]> {
    return await request<SearchTraceItem[]>(`/cases/${caseId}/traces`, {
      method: 'GET',
    });
  },

  /**
   * 导出权威 DOCX 查明与咨询意见书 (.docx)
   * 对应 GET /cases/{id}/export/docx
   */
  async exportDocx(caseId: string): Promise<Blob> {
    return await downloadBlob(`/cases/${caseId}/export/docx`);
  },

  /**
   * 获取案件 Multi-Agent 协作流实时轨迹
   * 对应 GET /cases/{id}/agent-workflow
   */
  async getAgentWorkflow(caseId: string): Promise<AgentWorkflowResponse> {
    return await request<AgentWorkflowResponse>(`/cases/${caseId}/agent-workflow`, {
      method: 'GET',
    });
  },

  /**
   * 智能追问 Copilot (Chatbot 对话，支持红方对抗演练)
   * 对应 POST /cases/{id}/chat
   */
  async chatWithCase(
    caseId: string,
    messages: CaseChatMessage[],
    roleView: string = 'practitioner',
    mode: 'neutral' | 'red_teaming' = 'neutral'
  ): Promise<CaseChatResponse> {
    return await request<CaseChatResponse>(`/cases/${caseId}/chat`, {
      method: 'POST',
      body: JSON.stringify({ messages, role_view: roleView, mode }),
    });
  },

  /**
   * 一键沉淀 Chat 探索成果至分析底稿 (B 包专家咨询准备或人工备忘)
   * 对应 POST /cases/{id}/insights
   */
  async saveCaseInsight(
    caseId: string,
    payload: SaveInsightPayload
  ): Promise<SavedInsight> {
    return await request<SavedInsight>(`/cases/${caseId}/insights`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  /**
   * 获取当前案件已沉淀的法律备忘与出庭质证成果清单
   * 对应 GET /cases/{id}/insights
   */
  async getCaseInsights(caseId: string): Promise<SavedInsight[]> {
    return await request<SavedInsight[]>(`/cases/${caseId}/insights`, {
      method: 'GET',
    });
  },

  /**
   * 订阅工作流实时事件流 (SSE)
   * 对应 GET /cases/{id}/events
   */
  subscribeEvents(
    caseId: string,
    onMessage: (event: string, data: any) => void,
    onError?: (error: any) => void
  ): () => void {
    const url = `/api/cases/${caseId}/events`;
    const eventSource = new EventSource(url);

    eventSource.addEventListener('connected', (e) => {
      try {
        onMessage('connected', JSON.parse(e.data));
      } catch {
        onMessage('connected', e.data);
      }
    });

    eventSource.addEventListener('node_start', (e) => {
      try {
        onMessage('node_start', JSON.parse(e.data));
      } catch {
        onMessage('node_start', e.data);
      }
    });

    eventSource.addEventListener('state_update', (e) => {
      try {
        onMessage('state_update', JSON.parse(e.data));
      } catch {
        onMessage('state_update', e.data);
      }
    });

    eventSource.addEventListener('done', (e) => {
      try {
        onMessage('done', JSON.parse(e.data));
      } catch {
        onMessage('done', e.data);
      }
    });

    eventSource.addEventListener('error', (err) => {
      if (onError) onError(err);
    });

    return () => {
      eventSource.close();
    };
  },

  /**
   * 阶段流转：投前合规审查 <-> 履约索赔与争议
   * 对应 POST /cases/{id}/transition-stage
   */
  async transitionStage(
    caseId: string,
    payload: {
      target_stage: 'pre_investment' | 'execution_dispute';
      transition_note?: string;
      override_title?: string;
      project_archetypes?: string[];
    }
  ): Promise<CaseState> {
    return await request<CaseState>(`/cases/${caseId}/transition-stage`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  /**
   * 工程合规与争议交互式沙盘试算接口 (What-If Engineering Simulation)
   * 对应 POST /cases/{id}/simulate-engineering
   */
  async simulateEngineering(
    caseId: string,
    params: {
      declared_tkdn_pct?: number;
      delay_days?: number;
      notice_days?: number;
      sinosure_notice_days?: number;
      main_ld_cap_pct?: number;
      sub_ld_cap_pct?: number;
      foreign_equity_pct?: number;
    }
  ): Promise<CaseState> {
    return await request<CaseState>(`/cases/${caseId}/simulate-engineering`, {
      method: 'POST',
      body: JSON.stringify(params),
    });
  },

  /**
   * 获取支持的法域元数据
   * 对应 GET /jurisdictions
   */
  async getJurisdictions(activeOnly: boolean = true): Promise<any[]> {
    return await request<any[]>('/jurisdictions', {
      method: 'GET',
      params: { active_only: activeOnly },
    });
  },

  /**
   * 获取东盟出海建设工程五阶段 × 三道防线合规指南
   * 对应 GET /compliance/guidelines
   */
  async getComplianceGuidelines(): Promise<any[]> {
    return await request<any[]>('/compliance/guidelines', {
      method: 'GET',
    });
  },

  /**
   * 获取东盟六国涉外基建横向对比矩阵
   * 对应 GET /compliance/comparison-matrix
   */
  async getComparisonMatrix(): Promise<any[]> {
    return await request<any[]>('/compliance/comparison-matrix', {
      method: 'GET',
    });
  },

  /**
   * 获取东盟国别风险预警矩阵
   * 对应 GET /compliance/risk-matrix
   */
  async getRiskMatrix(jurisdiction?: string): Promise<any> {
    return await request<any>('/compliance/risk-matrix', {
      method: 'GET',
      params: jurisdiction ? { jurisdiction } : undefined,
    });
  },

  /**
   * 获取东盟出海典型工程示范案库
   * 对应 GET /compliance/reference-cases
   */
  async getReferenceCases(): Promise<any[]> {
    return await request<any[]>('/compliance/reference-cases', {
      method: 'GET',
    });
  },

  /**
   * 建案前原始邮件/索赔通知函/投资备忘录一键智能要素抽提
   * 对应 POST /cases/extract-intake
   */
  async extractCaseIntake(payload: { raw_text: string; hint_jurisdiction?: string }): Promise<IntakeExtractResponse> {
    return await request<IntakeExtractResponse>('/cases/extract-intake', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  /**
   * 将外部工具箱成果（合同红线体检、重点法条引证、专家避冲记录）一键挂载至案卷
   * 对应 POST /cases/{id}/attach-artifact
   */
  async attachCaseArtifact(
    caseId: string,
    payload: {
      artifact_type: 'redline_scan' | 'statute_pin' | 'expert_coi';
      title: string;
      jurisdiction?: string;
      summary: string;
      redline_clause?: string;
      details?: Record<string, any>;
    }
  ): Promise<AttachedArtifact[]> {
    return await request<AttachedArtifact[]>(`/cases/${caseId}/attach-artifact`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  /**
   * 从案卷中移除已挂载的工具成果
   * 对应 DELETE /cases/{id}/attach-artifact/{artifactId}
   */
  async removeCaseArtifact(caseId: string, artifactId: string): Promise<AttachedArtifact[]> {
    return await request<AttachedArtifact[]>(`/cases/${caseId}/attach-artifact/${artifactId}`, {
      method: 'DELETE',
    });
  },

  /**
   * 解析上传的 .docx / .txt / .md 文件并提取纯文本
   * 对应 POST /cases/parse-doc
   */
  async parseDocument(file: File): Promise<{ filename: string; text: string; char_count: number }> {
    const formData = new FormData();
    formData.append('file', file);
    return await request<{ filename: string; text: string; char_count: number }>('/cases/parse-doc', {
      method: 'POST',
      body: formData,
    });
  },
};



