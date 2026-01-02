// API Types Definition
export interface ImageProcessingOptions {
    ratio: '4:5' | '1:1' | '16:9';
    backgroundColor?: string;
    style: 'minimal' | 'mood' | 'street';
    enhanceColor?: boolean;
    removeWrinkles?: boolean;
}

export interface ProcessingResponse {
    blob: Blob;
    headers: {
        processingTime: number;
        processingStyle: string;
        outputFormat: string;
        timingBackground: number;
        timingStyle: number;
    };
}

export interface ImageInfo {
    size: [number, number];
    width: number;
    height: number;
    mode: string;
    format: string;
    aspectRatio: number;
    filename: string;
    contentType: string;
}

export interface HealthCheckResponse {
    status: 'healthy' | 'unhealthy';
    model_loaded: boolean;
    styles_available: string[];
}
