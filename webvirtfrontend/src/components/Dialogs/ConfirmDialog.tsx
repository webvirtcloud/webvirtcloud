import ExclamationTriangleIcon from '@heroicons/react/20/solid/ExclamationTriangleIcon';
import tw from 'twin.macro';

import { Button } from '@/components/Button';
import { Dialog } from '@/components/Dialog';

type Props = {
  title: string;
  isOpen: boolean;
  isConfirmButtonLoading: boolean;
  onToggle: (state: boolean) => void;
  onConfirm: () => void;
};

const ConfirmDialog = ({
  title,
  isOpen,
  isConfirmButtonLoading,
  onToggle,
  onConfirm,
}: Props) => {
  return (
    <Dialog title={title} isOpen={isOpen} onClose={() => onToggle(false)}>
      <ExclamationTriangleIcon css={tw`mx-auto text-red-500`} width={32} height={32} />
      <p css={tw`mb-4 text-center text-gray-400`}>
        This action will permanently remove this item.
      </p>
      <div css={tw`grid grid-cols-2 gap-4 pt-4`}>
        <Button variant="secondary" onClick={() => onToggle(false)}>
          Close
        </Button>
        <Button
          loading={isConfirmButtonLoading}
          variant="danger"
          onClick={() => onConfirm()}
        >
          Confirm
        </Button>
      </div>
    </Dialog>
  );
};

export default ConfirmDialog;
