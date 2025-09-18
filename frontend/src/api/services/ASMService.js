import { apiClient } from "../client/APIClient"

class ASMService {
    static #URL = "/asm";

    async getModifiers() {
        return apiClient.get(`${ASMService.#URL}/modifiers`);
    }

    async getSeizureTypes() {
        return apiClient.get(`${ASMService.#URL}/seizure-types`);
    }

    async selection(data) {
        return apiClient.post(`${ASMService.#URL}/selection`, data)
    }

}

export const asmService = new ASMService();