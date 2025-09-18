import { useMutation } from "@tanstack/react-query"
import { asmService } from "../services/ASMService"

export function useASMSelection({ onSuccess }) {

  return useMutation({
    mutationKey: ["selection"],
    mutationFn: async (data) => {
      const res = await asmService.selection(data);
      return res.data;
    },
    onSuccess: (data) => {
      console.log('[DEBUG] Received selection data:', data);
      onSuccess?.(data);   // ← уведомляем родителя
    },
  })
}
