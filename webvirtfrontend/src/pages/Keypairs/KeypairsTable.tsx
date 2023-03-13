import { format } from 'date-fns';
import { useState } from 'react';
import tw from 'twin.macro';

import { Keypair } from '@/api/keypairs';
import { Button } from '@/components/Button';
import ConfirmDialog from '@/components/Dialogs/ConfirmDialog';
import EditKeypairDialog from '@/components/Dialogs/EditKeypair';

type Props = {
  data: { keypairs: Keypair[] } | undefined;
  error: any;
  onUpdate: (keypair: Keypair) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
};

export const KeypairsTable = ({ data, error, onUpdate, onDelete }: Props) => {
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [selectedKeypair, setSelectedKeypair] = useState<Keypair>();

  const onConfirmDelete = (id: number) => {
    setIsDeleting(true);
    return onDelete(id).then(() => setIsDeleteDialogOpen(false));
  };

  const handleClickOnEditAction = (key: Keypair) => {
    setSelectedKeypair(key);
    setIsEditDialogOpen(true);
  };

  const handleClickOnDeleteAction = (key: Keypair) => {
    setSelectedKeypair(key);
    setIsDeleteDialogOpen(true);
  };

  return (
    <div>
      <div css={tw`border divide-y rounded-md bg-base`}>
        {data && data.keypairs.length > 0 ? (
          data.keypairs.map((key) => (
            <div key={key.id} css={tw`flex flex-wrap items-center gap-24 p-4 text-alt2`}>
              <div css={tw`font-bold text-body`}>{key.name}</div>
              <div>{key.fingerprint}</div>
              <div>Added on {format(new Date(key.created_at), 'MMM dd, yyyy')}</div>
              <div css={tw`ml-auto space-x-2`}>
                <Button variant="secondary" onClick={() => handleClickOnEditAction(key)}>
                  Edit
                </Button>
                <Button variant="danger" onClick={() => handleClickOnDeleteAction(key)}>
                  Delete
                </Button>
              </div>
            </div>
          ))
        ) : (
          <p css={tw`p-8 text-center`}>No keypairs found!</p>
        )}
        {error && (
          <p css={tw`p-4 font-bold text-center`}>
            Something goes wrong...Try again later.
          </p>
        )}
      </div>
      <ConfirmDialog
        title="Delete key pair?"
        isOpen={isDeleteDialogOpen}
        isConfirmButtonLoading={isDeleting}
        onToggle={setIsDeleteDialogOpen}
        onConfirm={() => selectedKeypair && onConfirmDelete(selectedKeypair.id)}
      />
      <EditKeypairDialog
        isOpen={isEditDialogOpen}
        keypair={selectedKeypair}
        onToggle={setIsEditDialogOpen}
        onUpdate={onUpdate}
      />
    </div>
  );
};
