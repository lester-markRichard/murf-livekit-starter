export interface AppConfig {
  pageTitle: string;
  pageDescription: string;
  companyName: string;

  supportsChatInput: boolean;
  supportsVideoInput: boolean;
  supportsScreenShare: boolean;
  isPreConnectBufferEnabled: boolean;

  logo: string;
  startButtonText: string;
  accent?: string;
  logoDark?: string;
  accentDark?: string;

  audioVisualizerType?: 'bar' | 'wave' | 'grid' | 'radial' | 'aura';
  audioVisualizerColor?: `#${string}`;
  audioVisualizerColorDark?: `#${string}`;
  audioVisualizerColorShift?: number;
  audioVisualizerBarCount?: number;
  audioVisualizerGridRowCount?: number;
  audioVisualizerGridColumnCount?: number;
  audioVisualizerRadialBarCount?: number;
  audioVisualizerRadialRadius?: number;
  audioVisualizerWaveLineWidth?: number;

  agentName?: string;
  sandboxId?: string;
}

export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'हिंदी सीखो | Learn Hindi',
  pageTitle: 'Hindi-English Learning Tutor',
  pageDescription: 'बच्चों के लिए मजेदार हिंदी सीखने का अनुभव | Fun Hindi learning for children',

  supportsChatInput: false,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '/murf-logo.svg',
  accent: '#F59E0B',
  logoDark: '/murf-logo-dark.svg',
  accentDark: '#FBBF24',
  startButtonText: 'शुरू करो | Start',

  audioVisualizerType: 'bar',
  audioVisualizerColor: '#F59E0B',
  audioVisualizerColorDark: '#FBBF24',
  audioVisualizerColorShift: 0.2,
  audioVisualizerBarCount: 7,

  agentName: process.env.AGENT_NAME ?? undefined,
  sandboxId: undefined,
};
