//     // Fetch subject and snippet for each message
//     const suggestions = await Promise.all(
//       messages.map(async (msg) => {
//         const msgDetails = await gmail.users.messages.get({
//           userId: 'me',
//           id: msg.id,
//         });
//         return {
//           id: msg.id,
//           subject: msgDetails.data.payload.headers.find(header => header.name === 'Subject')?.value || '(No Subject)',
//           snippet: msgDetails.data.snippet,
//         };
//       })
//     );