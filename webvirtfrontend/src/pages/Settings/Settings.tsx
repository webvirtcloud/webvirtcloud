import tw from 'twin.macro';

import ChangePasswordForm from './ChangePasswordForm';
import UpdateProfileForm from './UpdateProfileForm';

const Settings = (): JSX.Element => {
  return (
    <>
      <h1 css={tw`mb-8 text-xl font-bold`}>Settings</h1>

      <section css={tw`space-y-8`}>
        <div css={tw`grid grid-cols-5 gap-8 p-8 border bg-base rounded-xl`}>
          <div css={tw`col-span-2`}>
            <h2 css={tw`mb-2 text-lg font-bold`}>Profile</h2>
            <p css={tw`text-alt2`}>Update information about your profile.</p>
          </div>
          <div css={tw`col-span-3`}>
            <UpdateProfileForm />
          </div>
        </div>

        <div css={tw`grid grid-cols-5 gap-8 p-8 border bg-base rounded-xl`}>
          <div css={tw`col-span-2`}>
            <h2 css={tw`mb-2 text-lg font-bold`}>Password</h2>
            <p css={tw`text-alt2`}>
              You can change your current password to new one. After submitting the form
              you will be redirected to the Sign In page.
            </p>
          </div>
          <div css={tw`col-span-3`}>
            <ChangePasswordForm />
          </div>
        </div>
      </section>
    </>
  );
};

export default Settings;
