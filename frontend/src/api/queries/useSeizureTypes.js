import { useQuery } from "@tanstack/react-query";
import { asmService } from "../services/ASMService"


export function useSeizureTypes() {
  return useQuery({
    queryKey: ["seizureTypes"],
    queryFn: asmService.getSeizureTypes,
    staleTime: 1000 * 60 * 60, // 1 hour
    select: data => data.data,
  });
}