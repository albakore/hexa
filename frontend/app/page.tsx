import NodeFlow from "@/components/node_flow/NodeFlow";
import { ColorModeButton } from "@/components/ui/color-mode";
import { Box, VStack } from "@chakra-ui/react";

export default function Home() {
  return (
    <Box as={'main'}>
      <NodeFlow/>
      <ColorModeButton
        position={'fixed'}
        top={'10px'}
        right={'10px'} />
    
    </Box>
  );
}
