import { useAtom } from 'jotai';
import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import tw from 'twin.macro';

import type { Profile } from '@/api/account';
import { updateProfile } from '@/api/account';
import { Button } from '@/components/Button';
import Input from '@/components/Input';
import { useToastContext } from '@/components/Toast';
import { useProfileStore } from '@/store/profile';

const UpdateProfileForm = (): JSX.Element => {
  const [profile] = useAtom(useProfileStore);

  const createToast = useToastContext();

  const {
    register,
    handleSubmit,
    setValue,
    trigger,
    formState: { isSubmitting, isValid, errors },
  } = useForm<Profile>({ mode: 'onChange' });

  const setDefaultValues = (profile: Profile) => {
    setValue('email', profile.email);
    setValue('first_name', profile.first_name);
    setValue('last_name', profile.last_name);

    trigger(['email', 'first_name', 'last_name']);
  };

  const onSubmit = async (data: Profile) => {
    try {
      const response = await updateProfile(data);

      setDefaultValues(response.profile);

      createToast({ type: 'success', message: 'Your profile was updated.' });
    } catch (error) {}
  };

  useEffect(() => {
    profile && setDefaultValues(profile);
  }, [profile]);

  return (
    <form onSubmit={handleSubmit(onSubmit)} css={tw`space-y-4`}>
      <Input
        {...register('email')}
        readonly
        placeholder="Your email"
        label="Email"
        id="email"
        name="email"
        size="lg"
        hint="Cannot be changed."
      />
      <div css={tw`grid grid-cols-2 gap-4`}>
        <Input
          {...register('first_name', { required: 'First name is required.' })}
          placeholder="John"
          label="First name"
          id="first_name"
          name="first_name"
          size="lg"
          required
          error={errors.first_name?.message}
        />
        <Input
          {...register('last_name', { required: 'Last name is required.' })}
          placeholder="Doe"
          label="Last name"
          id="last_name"
          name="last_name"
          size="lg"
          required
          error={errors.last_name?.message}
        />
      </div>
      <Button
        size="lg"
        loading={isSubmitting}
        disabled={!isValid}
        css={tw`w-full`}
        type="submit"
      >
        Update profile
      </Button>
    </form>
  );
};

export default UpdateProfileForm;
