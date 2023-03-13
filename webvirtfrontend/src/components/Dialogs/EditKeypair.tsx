import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import tw from 'twin.macro';

import type { Keypair, KeypairPayload } from '@/api/keypairs';
import { updateKeypair } from '@/api/keypairs';
import { Button } from '@/components/Button';
import { Dialog } from '@/components/Dialog';
import Input from '@/components/Input';
import Textarea from '@/components/Textarea';

type Props = {
  isOpen: boolean;
  keypair: Keypair | undefined;
  onToggle: (state: boolean) => void;
  onUpdate: (keypair: Keypair) => void;
};

const EditKeypairDialog = ({ isOpen, keypair, onToggle, onUpdate }: Props) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<KeypairPayload>({ mode: 'onChange' });

  useEffect(() => {
    if (keypair) {
      reset(keypair);
    }
  }, [keypair]);

  const onSubmit = async (data: KeypairPayload) => {
    try {
      if (keypair === undefined) return;

      const updatedKeypair = await updateKeypair(keypair.id, { name: data.name }).then(
        (response) => response.keypair,
      );
      onUpdate(updatedKeypair);
      onToggle(false);
    } catch (error) {}
  };

  return (
    <Dialog title="Edit Keypair" isOpen={isOpen} onClose={() => onToggle(false)}>
      <form onSubmit={handleSubmit(onSubmit)} css={tw`space-y-4`}>
        <div>
          <Input
            id="name"
            {...register('name', { required: 'Name of Keypair is required.' })}
            label="Name"
            placeholder="My access key"
            required
            error={errors.name?.message}
          />
        </div>
        <div>
          <Textarea
            id="public_key"
            rows={10}
            readOnly
            spellCheck={false}
            {...register('public_key', { required: 'Public key is required.' })}
            label="Public key"
            placeholder="Your public key"
            required
            error={errors.public_key?.message}
          ></Textarea>
        </div>
        <Button type="submit" fullWidth size="lg" loading={isSubmitting}>
          Submit
        </Button>
      </form>
    </Dialog>
  );
};

export default EditKeypairDialog;
