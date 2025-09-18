import { useQuery } from "@tanstack/react-query";
import { asmService } from "../services/ASMService"


export function useModifiers() {
  return useQuery({
    queryKey: ["modifiers"],
    queryFn: asmService.getModifiers,
    staleTime: 1000 * 60 * 60, // 1 hour,
    select: data => data.data,
  });
}